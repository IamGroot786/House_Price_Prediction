import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
css_path = os.path.join(BASE_DIR, "css", "style.css")

def load_css():
    with open(css_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="Login")
load_css()

st.title("Login to House Price Predictor")

if 'users' not in st.session_state:
    st.session_state.users = {}

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Logged in successfully!")
        st.switch_page("app.py")
    else:
        st.error("Invalid credentials")

st.page_link("pages/register.py", label="Don't have an account? Register here")