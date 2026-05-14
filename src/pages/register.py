import streamlit as st
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="house_price_prediction"
    )

st.title("📝 Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        st.error("Username already exists")

    else:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        st.success("Account created! Please login.")
        st.switch_page("pages/login.py")

    cursor.close()
    conn.close()