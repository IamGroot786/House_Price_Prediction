import streamlit as st
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="house_price_prediction"
    )

def show_profile(navigate):

    st.title("👤 Profile")

    st.info(f"Username: {st.session_state.username}")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Update"):

        conn = connect_db()
        cursor = conn.cursor()

        if new_username:
            cursor.execute(
                "UPDATE users SET username=%s WHERE username=%s",
                (new_username, st.session_state.username)
            )
            st.session_state.username = new_username

        if new_password:
            cursor.execute(
                "UPDATE users SET password=%s WHERE username=%s",
                (new_password, st.session_state.username)
            )

        conn.commit()
        cursor.close()
        conn.close()

        st.success("Updated successfully")

    if st.button("Back"):
        navigate("home")