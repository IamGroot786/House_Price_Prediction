# ------------------ 1. IMPORTS ------------------
import streamlit as st
import pandas as pd
import joblib
import os
from components.header import render_header
from components.footer import render_footer
from pages.landing_page import show_home
from pages.profile import show_profile
from PIL import Image

# ------------------ 2. PATHS ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "house_price_model.pkl")
css_path = os.path.join(BASE_DIR, "css", "style.css")

# ------------------ 3. LOAD MODEL (SAFE) ------------------
if not os.path.exists(model_path):
    st.error("❌ Model file not found. Please train and save the model first.")
    st.stop()

model = joblib.load(model_path)

# ------------------ 4. LOAD CSS ------------------
def load_css():
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
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

# ------------------ 7. NAVIGATION ------------------
def navigate(page):
    st.session_state.page = page
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
            st.switch_page("pages/login.py")

with col4:
    if st.session_state.get("logged_in", False):
        if st.button("Profile"):
            navigate("profile")

with col5:
    if st.session_state.get("logged_in", False):
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
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
        st.session_state.logged_in = False
        st.rerun()

    # ------------------ HERO ------------------
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c", width="stretch")

    st.markdown('<div class="title">🏠 Estimate Property Price</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; font-size: 18px; color: #666;">
    Get accurate property price estimates using advanced AI technology. 
    Enter your property details below to receive instant valuations.
    </div>
    """, unsafe_allow_html=True)

    # ------------------ FORM ------------------
    st.markdown("## 📝 Property Details")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div>', unsafe_allow_html=True)

        transaction_type = st.selectbox("Transaction Type", ["Buy Property", "Rent Property"])
        house_type = st.selectbox("House Type", ["Flat", "Studio Flat", "PG", "Bungalow"])
        location_option = st.selectbox("Location Tier", ["Tier 1 City", "Tier 2 City", "Tier 3 City"])

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div>', unsafe_allow_html=True)

        area = st.number_input("Area (sq ft)", 200, 10000, value=1000)
        bedrooms = st.number_input("Bedrooms", 1, 10, value=2)
        bathrooms = st.number_input("Bathrooms", 1, 10, value=2)

        floors = parking = garden = sharing = meal_included = building_age = 0

        if house_type == "Bungalow":
            floors = st.number_input("Floors", 1, 5)
            garden = st.selectbox("Garden", ["No", "Yes"])

        elif house_type == "PG":
            sharing = st.selectbox("Sharing", ["Single", "Double", "Triple"])
            meal_included = st.selectbox("Meal Included", ["No", "Yes"])

        elif house_type == "Studio Flat":
            building_age = st.number_input("Building Age", 0, 50)

        elif house_type == "Flat":
            parking = st.number_input("Parking", 0, 5)

        budget = st.number_input("Your Budget (₹)", 0, value=5000000)

        if st.button("🚀 Estimate Price"):

            garden = 1 if garden == "Yes" else 0
            meal_included = 1 if meal_included == "Yes" else 0

            sharing_map = {"Single":1, "Double":2, "Triple":3}
            sharing = sharing_map.get(sharing, 0)

            house_map = {"Flat":0, "Studio Flat":1, "PG":2, "Bungalow":3}
            house_type_encoded = house_map[house_type]

            input_data = pd.DataFrame({
                "area":[area],
                "bedrooms":[bedrooms],
                "bathrooms":[bathrooms],
                "floors":[floors],
                "parking":[parking],
                "garden":[garden],
                "sharing":[sharing],
                "meal_included":[meal_included],
                "building_age":[building_age],
                "house_type":[house_type_encoded]
            })

            prediction = model.predict(input_data)[0]

            location_multiplier = {
                "Tier 1 City": 1.5,
                "Tier 2 City": 1.2,
                "Tier 3 City": 0.9
            }

            prediction *= location_multiplier[location_option]

            if transaction_type == "Rent Property":
                prediction *= 0.005

            st.success(f"💰 Estimated Price: ₹ {round(prediction,2):,}")

            if budget > 0:
                diff = prediction - budget
                if diff > 0:
                    st.error(f"Over budget by ₹ {round(diff,2):,}")
                else:
                    st.success(f"Within budget! Saving ₹ {round(abs(diff),2):,}")

        st.markdown('</div>', unsafe_allow_html=True)


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