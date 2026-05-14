import streamlit as st
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="house_price_prediction"
    )

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user is None:
        st.error("User not found")

    elif user[1] != password:
        st.error("Incorrect password")

    else:
        st.session_state.logged_in = True
        st.session_state.username = user[0]
        st.success("Login successful")
        st.switch_page("app.py")

    cursor.close()
    conn.close()

st.page_link("pages/register.py", label="Create Account")