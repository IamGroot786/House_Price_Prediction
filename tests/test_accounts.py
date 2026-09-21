import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import accounts
from mysql.connector import Error, IntegrityError


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = self.connection.cursor.return_value
        self.connect = patch("accounts.connect_db", return_value=self.connection).start()
        self.addCleanup(patch.stopall)

    def test_hashes_are_salted_and_verify(self):
        first = accounts.hash_password("secret")
        second = accounts.hash_password("secret")
        self.assertNotEqual(first, second)
        self.assertLessEqual(len(first), 255)
        self.assertTrue(accounts.verify_password("secret", first))
        self.assertFalse(accounts.verify_password("incorrect", first))
        self.assertFalse(accounts.verify_password("secret", "pbkdf2_sha256$broken"))

    def test_legacy_passwords_remain_usable(self):
        self.assertTrue(accounts.verify_password("secret", "secret"))
        self.assertFalse(accounts.verify_password("incorrect", "secret"))

    def test_empty_credentials_do_not_connect(self):
        for username, password in [("  ", "password"), ("alice", "  "), ("x" * 31, "pass")]:
            with self.subTest(username=username), self.assertRaises(accounts.AccountError):
                accounts.register_account(username, password)
        self.connect.assert_not_called()

    def test_login_releases_database_before_returning(self):
        self.cursor.fetchone.return_value = ("alice", "secret")
        self.assertEqual(accounts.authenticate(" alice ", "secret"), "alice")
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_invalid_login_does_not_expose_account_existence(self):
        for result in [None, ("alice", "secret")]:
            self.cursor.fetchone.return_value = result
            with self.assertRaisesRegex(accounts.AccountError, "Incorrect username or password"):
                accounts.authenticate("alice", "wrong")

    def test_registration_stores_hash(self):
        self.cursor.fetchone.return_value = None
        accounts.register_account(" alice ", "secret")
        query, params = self.cursor.execute.call_args.args
        self.assertIn("INSERT", query)
        self.assertEqual(params[0], "alice")
        self.assertTrue(accounts.verify_password("secret", params[1]))
        self.connection.commit.assert_called_once()
        self.connection.close.assert_called_once()

    def test_duplicate_registration_rolls_back(self):
        self.cursor.fetchone.return_value = ("alice",)
        with self.assertRaisesRegex(accounts.AccountError, "already exists"):
            accounts.register_account("alice", "secret")
        self.connection.commit.assert_not_called()
        self.connection.rollback.assert_called_once()
        self.connection.close.assert_called_once()

    def test_concurrent_duplicate_insert_is_reported(self):
        self.cursor.fetchone.return_value = None
        self.cursor.execute.side_effect = [None, IntegrityError(errno=1062)]
        with self.assertRaisesRegex(accounts.AccountError, "already exists"):
            accounts.register_account("alice", "secret")
        self.connection.commit.assert_not_called()

    def test_profile_rename_and_password_update_are_atomic(self):
        self.cursor.fetchone.side_effect = [("alice",), None]
        self.assertEqual(accounts.update_account("alice", "bob", "new secret"), "bob")
        query, params = self.cursor.execute.call_args.args
        self.assertIn("username=%s, password=%s", query)
        self.assertEqual((params[0], params[2]), ("bob", "alice"))
        self.assertTrue(accounts.verify_password("new secret", params[1]))
        self.connection.commit.assert_called_once()

    def test_profile_duplicate_name_does_not_update_password(self):
        self.cursor.fetchone.side_effect = [("alice",), ("bob",)]
        with self.assertRaisesRegex(accounts.AccountError, "already exists"):
            accounts.update_account("alice", "bob", "new secret")
        self.assertFalse(any(call.args[0].startswith("UPDATE") for call in self.cursor.execute.call_args_list))
        self.connection.commit.assert_not_called()

    def test_commit_failure_rolls_back_and_closes(self):
        self.cursor.fetchone.side_effect = [("alice",), None]
        self.connection.commit.side_effect = Error(errno=2013)
        with self.assertRaises(accounts.AccountError):
            accounts.update_account("alice", "bob", "")
        self.connection.rollback.assert_called_once()
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_missing_account_cannot_report_success(self):
        self.cursor.fetchone.return_value = None
        with self.assertRaisesRegex(accounts.AccountError, "no longer exists"):
            accounts.update_account("alice", "bob", "")

    def test_empty_profile_update_is_rejected(self):
        for username, password in [("", ""), (" ", ""), ("", " ")]:
            with self.assertRaises(accounts.AccountError):
                accounts.update_account("alice", username, password)
        self.connect.assert_not_called()

    def test_database_outage_has_actionable_error(self):
        self.connect.side_effect = Error(errno=2003)
        with self.assertRaisesRegex(accounts.AccountError, "database is unavailable"):
            accounts.authenticate("alice", "secret")


if __name__ == "__main__":
    unittest.main()
