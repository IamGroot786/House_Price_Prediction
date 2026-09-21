"""Account storage shared by the login, registration, and profile pages."""

from contextlib import contextmanager
import hashlib
import hmac
import logging
import os
import secrets

import mysql.connector
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


class AccountError(Exception):
    """A message that can safely be displayed to the user."""


def connect_db():
    try:
        settings = st.secrets.get("mysql", {})
    except StreamlitSecretNotFoundError:
        settings = {}
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", settings.get("host", "localhost")),
        port=int(os.getenv("DB_PORT", settings.get("port", "3306"))),
        user=os.getenv("DB_USER", settings.get("user", "root")),
        password=os.getenv("DB_PASSWORD", settings.get("password", "")),
        database=os.getenv("DB_NAME", settings.get("database", "house_price_prediction")),
        connection_timeout=5,
    )


@contextmanager
def database():
    """Finish transactions and release connections before any page redirect."""
    conn = cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True)
        yield cursor
        conn.commit()
    except mysql.connector.IntegrityError as exc:
        if exc.errno == 1062:
            raise AccountError("Username already exists. Choose another username.") from exc
        raise AccountError("The account could not be saved. Check the database setup.") from exc
    except mysql.connector.Error as exc:
        logging.getLogger(__name__).warning("Account database error: %s", exc.errno)
        raise AccountError(
            "The account database is unavailable or incorrectly configured. "
            "Check the MySQL service and database setup in README.md."
        ) from exc
    except ValueError as exc:
        raise AccountError("Invalid database configuration. Check DB_PORT.") from exc
    finally:
        if conn is not None:
            try:
                # Roll back any uncommitted work, including a failed commit.
                conn.rollback()
            except mysql.connector.Error:
                pass
        if cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error:
                pass
        if conn is not None:
            try:
                conn.close()
            except mysql.connector.Error:
                pass


def validate_username(username):
    username = username.strip()
    if not username:
        raise AccountError("Enter a username.")
    if len(username) > 30:
        raise AccountError("Username must be 30 characters or fewer.")
    return username


def validate_password(password):
    if not password.strip():
        raise AccountError("Enter a password containing more than spaces.")


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), 600_000)
    return f"pbkdf2_sha256$600000${salt}${digest.hex()}"


def verify_password(password, stored):
    if not isinstance(stored, str):
        return False
    if not stored.startswith("pbkdf2_sha256$"):
        # Changing an existing account's password upgrades its legacy storage.
        return hmac.compare_digest(password.encode("utf-8"), stored.encode("utf-8"))
    try:
        _, iterations, salt, expected = stored.split("$")
        if int(iterations) != 600_000:
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), int(iterations))
        return hmac.compare_digest(digest.hex(), expected)
    except (ValueError, UnicodeError):
        return False


def authenticate(username, password):
    username = validate_username(username)
    validate_password(password)
    with database() as cursor:
        cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
    if user is None or not verify_password(password, user[1]):
        raise AccountError("Incorrect username or password.")
    return user[0]


def register_account(username, password):
    username = validate_username(username)
    validate_password(password)
    password_hash = hash_password(password)
    with database() as cursor:
        cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            raise AccountError("Username already exists. Choose another username.")
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password_hash),
        )
    return username


def update_account(username, new_username, new_password):
    if not new_username and not new_password:
        raise AccountError("Enter a new username or password before updating.")
    target_username = validate_username(new_username) if new_username else username
    if new_password:
        validate_password(new_password)
    password_hash = hash_password(new_password) if new_password else None
    with database() as cursor:
        cursor.execute("SELECT username FROM users WHERE username=%s FOR UPDATE", (username,))
        if cursor.fetchone() is None:
            raise AccountError("This account no longer exists. Please log in again.")
        if target_username != username:
            cursor.execute("SELECT username FROM users WHERE username=%s", (target_username,))
            if cursor.fetchone():
                raise AccountError("Username already exists. Choose another username.")
        if password_hash is not None:
            cursor.execute(
                "UPDATE users SET username=%s, password=%s WHERE username=%s",
                (target_username, password_hash, username),
            )
        else:
            cursor.execute("UPDATE users SET username=%s WHERE username=%s", (target_username, username))
    return target_username
