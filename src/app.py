# ------------------ 1. IMPORTS ------------------
import streamlit as st
import joblib
import os
from components.header import render_header
from components.footer import render_footer
from pages.landing_page import show_home
from pages.profile import show_profile
from components.prediction_design import render_prediction

# ------------------ 2. PATHS ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "house_price_model.pkl")
css_path = os.path.join(BASE_DIR, "css", "style.css")

# ------------------ 3. LOAD MODEL (SAFE) ------------------
@st.cache_resource
def load_model(path, modified_time):
    return joblib.load(path)

# ------------------ 4. LOAD CSS ------------------
def load_css():
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ------------------ 5. PAGE CONFIG ------------------
st.set_page_config(layout="wide")
load_css()
render_header()
# ------------------ 6. SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in and not st.session_state.get("username"):
    st.session_state.logged_in = False

if st.session_state.page not in {"home", "predict", "profile"}:
    st.session_state.page = "home"

# ------------------ 7. NAVIGATION ------------------
def navigate(page):
    st.session_state.page = page
    st.rerun()


def logout():
    st.session_state.clear()
    st.session_state.logged_in = False
    st.session_state.page = "home"
    st.rerun()

# ------------------ 8. NAVBAR ------------------
col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

with col1:
    st.markdown("")

with col2:
    if st.button("Home"):
        navigate("home")

with col3:
    if st.button("Predict"):
        if st.session_state.get("logged_in", False):
            navigate("predict")
        else:
            st.session_state.page = "predict"
            st.switch_page("pages/login.py")

with col4:
    if st.session_state.get("logged_in", False):
        if st.button("Profile"):
            navigate("profile")

with col5:
    if st.session_state.get("logged_in", False):
        if st.button("Logout"):
            logout()
    else:
        if st.button("Login"):
            st.switch_page("pages/login.py")

# ------------------ 9. ROUTING ------------------

# HOME
if st.session_state.page == "home":
    show_home(navigate)

# PROFILE
elif st.session_state.page == "profile":

    if not st.session_state.get("logged_in", False):
        st.warning("Please login first")
        st.switch_page("pages/login.py")

    show_profile(navigate)

# LOGIN CHECK
elif 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")

# PREDICT
elif st.session_state.page == "predict":

    st.sidebar.success(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        logout()

    if not os.path.exists(model_path):
        st.error("Model file not found. Please train and save the model first.")
    else:
        try:
            model = load_model(model_path, os.path.getmtime(model_path))
        except Exception:
            st.error("The prediction model could not be loaded. Check the model file and installed dependencies.")
        else:
            render_prediction(model)


# ------------------ PROPERTY GALLERY ------------------
st.markdown("---")
st.markdown("""
<div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; margin: 30px 0;">
    <h2 style="text-align: center; color: #2e8b57;">🏡 Featured Properties</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994")
    st.write("Luxury Villa")

with col2:
    st.image("https://images.unsplash.com/photo-1507089947367-19c1da9775ae")
    st.write("Modern Apartment")

with col3:
    st.image("https://images.unsplash.com/photo-1493809842364-78817add7ffb")
    st.write("Studio Space")

# ------------------ TESTIMONIALS SECTION ------------------
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #f0f8ff, #e6f7e6); padding: 40px; border-radius: 20px; margin: 30px 0;">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 30px;">💬 What Our Users Say</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="testimonial-card">
        <div class="stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"This tool saved me hours of research! The estimates were spot-on and helped me make an informed decision."</blockquote>
        <div class="author">- Rajesh Kumar, Mumbai</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial-card">
        <div class="stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"Incredibly accurate predictions! Used it for my property investment and the numbers matched market rates perfectly."</blockquote>
        <div class="author">- Priya Sharma, Delhi</div>
    </div>
    """, unsafe_allow_html=True)
    
# ------------------ 10. FOOTER ------------------
render_footer()
