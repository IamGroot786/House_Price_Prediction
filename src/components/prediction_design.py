import streamlit as st
import pandas as pd


def render_prediction(model):
    st.markdown('\n<style>\n.st-key-hpp_prediction {\nbackground:linear-gradient(115deg,rgba(236,245,255,.93),rgba(225,238,250,.8)),url(\'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1800&q=85\') center/cover;\npadding:48px 40px;border-radius:20px;border:1px solid #dce7f2;\n}\n.hpp-pred-heading {margin-bottom:30px;}\n.hpp-pred-heading h1 {color:#294f77;font-size:clamp(30px,4vw,56px);font-weight:750;letter-spacing:-.035em;line-height:1.15;margin:0 0 10px;}\n.hpp-pred-heading h1 span {color:#62ac7a;display:block;font-size:.8em;margin-top:12px;}\n.hpp-pred-heading p {color:#536f87;font-size:15px;line-height:1.7;max-width:620px;}\n.hpp-pred-art {padding:50px 0 20px;}\n.hpp-pred-art img {width:100%;height:290px;object-fit:cover;border-radius:100px 100px 22px 22px;border:8px solid #fff;box-shadow:0 22px 55px #39577620;}\n.hpp-pred-art h3 {color:#2b5374;font-size:24px;line-height:1.3;margin:24px 0 10px;}\n.hpp-pred-art p {color:#546e83;font-size:14px;line-height:1.75;}\n.hpp-pred-tag {display:inline-block;background:#fff;color:#3c6686;border-radius:30px;padding:8px 14px;font-size:11px;letter-spacing:.08em;margin-bottom:22px;}\n.st-key-hpp_prediction_form {background:rgba(250,250,255,.96);border:1px solid white;border-radius:22px;padding:28px;box-shadow:0 20px 65px #40618b24;}\n.st-key-hpp_prediction_form h2 {font-size:22px;color:#304963;}\n.st-key-hpp_prediction_form label p {color:#435872;font-size:13px;font-weight:600;}\n.st-key-hpp_prediction_form [data-baseweb="select"]>div,\n.st-key-hpp_prediction_form [data-baseweb="input"] {background:#fff;border-color:#e3e8f4;border-radius:8px;color:#203950;}\n.st-key-hpp_prediction_form input {color:#203950;background:#fff;}\n.st-key-hpp_prediction_form .stButton>button {background:#cdecd5;color:#287447;border-radius:10px;border:1px solid #bce2c7;box-shadow:none;width:100%;font-weight:700;}\n.st-key-hpp_prediction_form .stButton>button:hover {background:#b7e2c2;color:#1b5e35;transform:none;}\n.st-key-hpp_prediction_form .stButton>button:focus-visible {outline:3px solid #658eb2;outline-offset:3px;}\n.st-key-hpp_prediction_form [data-testid="stAlert"] {border-radius:12px;}\n@media(max-width:700px) {\n.st-key-hpp_prediction {padding:24px 16px;}\n.st-key-hpp_prediction_form {padding:18px;}\n.hpp-pred-art {padding:0;}\n.hpp-pred-art img {height:180px;border-radius:18px;}\n}\n</style>\n', unsafe_allow_html=True)
    with st.container(key="hpp_prediction"):
        st.markdown('\n<div class="hpp-pred-heading">\n<h1>House Price Prediction<span>using Machine Learning</span></h1>\n<p>Enter your property details below to receive an estimate and compare it with your budget.</p>\n</div>\n', unsafe_allow_html=True)
        illustration, details = st.columns([0.85, 1.8], gap="large")
        with illustration:
            st.markdown('\n<div class="hpp-pred-art">\n<span class="hpp-pred-tag">YOUR NEXT CHAPTER STARTS HERE</span>\n<img src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=85" alt="White house with a garden">\n<h3>A clearer picture.<br>A place to call home.</h3>\n<p>Explore a property estimate based on your selected details. Choose a purchase or rental scenario and see how it fits your budget.</p>\n</div>\n', unsafe_allow_html=True)
        with details:
            with st.container(key="hpp_prediction_form"):
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
