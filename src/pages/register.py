import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
css_path = os.path.join(BASE_DIR, "css", "style.css")

def load_css():
    with open(css_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="Register")
load_css()

st.title("Register for House Price Predictor")

if 'users' not in st.session_state:
    st.session_state.users = {}

username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Register"):
    if username in st.session_state.users:
        st.error("Username already exists")
    elif password != confirm_password:
        st.error("Passwords do not match")
    elif not username or not password:
        st.error("Please fill all fields")
    else:
        st.session_state.users[username] = password
        st.success("Registered successfully! Please log in.")
        st.switch_page("pages/login.py")

st.page_link("pages/login.py", label="Already have an account? Login here")