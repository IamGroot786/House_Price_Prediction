# ------------------ 1. IMPORTS ------------------
import streamlit as st
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "house_price_model.pkl")
css_path = os.path.join(BASE_DIR, "css", "style.css")

# ------------------ 2. LOAD MODEL ------------------
model = joblib.load(model_path)

# ------------------ 3. LOAD CSS ------------------
def load_css():
    with open(css_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ------------------ 4. PAGE CONFIG ------------------
st.set_page_config(layout="wide", page_title="House Price Predictor")
load_css()

# ------------------ 5. CHECK LOGIN ------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")

# ------------------ 6. MAIN APP ------------------
st.sidebar.success(f"Welcome, {st.session_state.username}!")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ------------------ 7. HERO SECTION ------------------
st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c", width="stretch")

st.markdown('<div class="title">🏠 Estimate Property Price</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; font-size: 18px; color: #666;">
Get accurate property price estimates using advanced AI technology. 
Enter your property details below to receive instant valuations.
</div>
""", unsafe_allow_html=True)

# ------------------ 8. FEATURES SECTION ------------------
st.markdown("""
<div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 30px;">✨ Why Choose Our Property Estimator?</h2>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎯</div>
        <h4>Accurate AI</h4>
        <p>Powered by machine learning for precise valuations</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">⚡</div>
        <h4>Instant Results</h4>
        <p>Get estimates in seconds, not days</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">📊</div>
        <h4>Market Insights</h4>
        <p>Based on current market trends</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">💰</div>
        <h4>Budget Analysis</h4>
        <p>Compare with your budget instantly</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ 9. FORM SECTION ------------------
st.markdown("## 📝 Property Details")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">📋 Basic Information</div>', unsafe_allow_html=True)

    transaction_type = st.selectbox(
        "Transaction Type", 
        ["Buy Property", "Rent Property"],
        help="Select whether you're buying or renting the property"
    )
    house_type = st.selectbox(
        "House Type", 
        ["Flat", "Studio Flat", "PG", "Bungalow"],
        help="Choose the type of property you're interested in"
    )
    location_option = st.selectbox(
        "Location Tier", 
        ["Tier 1 City", "Tier 2 City", "Tier 3 City"],
        help="Tier 1: Metro cities, Tier 2: Major cities, Tier 3: Smaller cities"
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🏗️ Specifications</div>', unsafe_allow_html=True)

    area = st.number_input(
        "Area (sq ft)", 
        200, 10000, 
        value=1000,
        help="Total built-up area of the property"
    )
    bedrooms = st.number_input(
        "Bedrooms", 
        1, 10, 
        value=2,
        help="Number of bedrooms in the property"
    )
    bathrooms = st.number_input(
        "Bathrooms", 
        1, 10, 
        value=2,
        help="Number of bathrooms in the property"
    )

    # Dynamic inputs based on house type
    floors = parking = garden = sharing = meal_included = building_age = 0

    if house_type == "Bungalow":
        st.markdown("### 🏡 Bungalow Details")
        floors = st.number_input("Floors", 1, 5, value=1, help="Number of floors in the bungalow")
        garden = st.selectbox("Garden", ["No", "Yes"], help="Does the bungalow have a garden?")
    elif house_type == "PG":
        st.markdown("### 🏢 PG Details")
        sharing = st.selectbox("Sharing Type", ["Single", "Double", "Triple"], help="Room sharing arrangement")
        meal_included = st.selectbox("Meal Included", ["No", "Yes"], help="Are meals included in rent?")
    elif house_type == "Studio Flat":
        st.markdown("### 🏠 Studio Details")
        building_age = st.number_input("Building Age (years)", 0, 50, value=5, help="Age of the building")
    elif house_type == "Flat":
        st.markdown("### 🏢 Flat Details")
        parking = st.number_input("Parking Spaces", 0, 5, value=1, help="Number of parking spaces available")

    st.markdown("### 💰 Budget Information")
    budget = st.number_input(
        "Your Budget (₹)", 
        0, 
        value=5000000,
        help="Enter your maximum budget for comparison"
    )

    if st.button("🚀 Estimate Price", type="primary"):
        # Convert categorical to numeric
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

        st.success(f"💰 **Estimated Price: ₹ {round(prediction,2):,}**")

        # Budget Analyzer
        if budget > 0:
            diff = prediction - budget
            if diff > 0:
                st.error(f"📉 **Over budget by ₹ {round(diff,2):,}**")
            else:
                st.success(f"✅ **Within budget! You save ₹ {round(abs(diff),2):,}**")

    st.markdown('</div>', unsafe_allow_html=True)
# ------------------ HOW IT WORKS SECTION ------------------
st.markdown("---")
st.markdown("""
<div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 30px;">🤖 How Our AI Works</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
        <h4 style="color: #2e8b57;">Data Analysis</h4>
        <p style="color: #666; font-size: 14px;">Trained on thousands of property transactions across different cities and property types</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 48px; margin-bottom: 15px;">🧠</div>
        <h4 style="color: #2e8b57;">Machine Learning</h4>
        <p style="color: #666; font-size: 14px;">Uses advanced algorithms to identify patterns and predict property values accurately</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 48px; margin-bottom: 15px;">📈</div>
        <h4 style="color: #2e8b57;">Market Trends</h4>
        <p style="color: #666; font-size: 14px;">Continuously updated with latest market data and location-based pricing factors</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
# ------------------ 10. PROPERTY GALLERY ------------------
st.markdown("---")
st.markdown("""
<div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 20px;">🏡 Featured Properties</h2>
    <p style="text-align: center; margin-bottom: 30px; color: #666;">Explore some beautiful properties in our featured collection</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="property-card card-hover">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994")
    st.markdown('<h4>🏡 Luxury Villa</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 14px; margin: 10px 0;">Spacious villa with modern amenities and garden</p>', unsafe_allow_html=True)
    st.markdown('<div style="color: #2e8b57; font-weight: bold; font-size: 18px;">₹2.5 Cr</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="property-card card-hover">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1507089947367-19c1da9775ae")
    st.markdown('<h4>🏢 Modern Apartment</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 14px; margin: 10px 0;">Contemporary apartment in prime location</p>', unsafe_allow_html=True)
    st.markdown('<div style="color: #2e8b57; font-weight: bold; font-size: 18px;">₹85 Lakhs</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="property-card card-hover">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1493809842364-78817add7ffb")
    st.markdown('<h4>🏠 Studio Space</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 14px; margin: 10px 0;">Cozy studio perfect for young professionals</p>', unsafe_allow_html=True)
    st.markdown('<div style="color: #2e8b57; font-weight: bold; font-size: 18px;">₹45 Lakhs</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 20px;">🧾 Houses on Sale</h2>
    <p style="text-align: center; margin-bottom: 30px; color: #666;">Browse featured sale listings with owner contact, home highlights, and pricing.</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="sale-card card-hover">
        <img class="sale-card__image" src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85" alt="Modern Family Home">
        <div class="sale-card__content">
            <h4>Modern Family Home</h4>
            <div class="sale-card__price">₹1.35 Cr</div>
            <div class="sale-card__owner">Owner: Sunita Verma</div>
            <div class="sale-card__contact">Contact: +91 98765 43210</div>
            <div class="sale-card__attributes">
                <span>4 BHK</span><span>3 Baths</span><span>2 Parking</span><span>2100 sq ft</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sale-card card-hover">
        <img class="sale-card__image" src="https://images.unsplash.com/photo-1494526585095-c41746248156" alt="City View Apartment">
        <div class="sale-card__content">
            <h4>City View Apartment</h4>
            <div class="sale-card__price">₹92 Lakhs</div>
            <div class="sale-card__owner">Owner: Arjun Mehta</div>
            <div class="sale-card__contact">Contact: +91 91234 56789</div>
            <div class="sale-card__attributes">
                <span>3 BHK</span><span>2 Baths</span><span>1 Parking</span><span>1450 sq ft</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="sale-card card-hover">
        <img class="sale-card__image" src="https://images.unsplash.com/photo-1494522358656-0d73f47029b9" alt="Cozy Suburban Villa">
        <div class="sale-card__content">
            <h4>Cozy Suburban Villa</h4>
            <div class="sale-card__price">₹1.12 Cr</div>
            <div class="sale-card__owner">Owner: Meera Joshi</div>
            <div class="sale-card__contact">Contact: +91 99876 54321</div>
            <div class="sale-card__attributes">
                <span>3 BHK</span><span>3 Baths</span><span>Garden</span><span>1850 sq ft</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ 11. TESTIMONIALS SECTION ------------------
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #f0f8ff, #e6f7e6); padding: 40px; border-radius: 20px; margin: 30px 0;">
    <h2 style="text-align: center; color: #2e8b57; margin-bottom: 30px;">💬 What Our Users Say</h2>
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

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ 12. FOOTER ------------------
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3>🏠 House Price Predictor</h3>
    <p>Empowering your real estate decisions with AI-powered insights</p>
    <p>© 2026 House Price Predictor | Built with ❤️ using Streamlit & Machine Learning</p>
</div>
""", unsafe_allow_html=True)

   