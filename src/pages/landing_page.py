import streamlit as st

def show_home(navigate):

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div style="
            padding:40px;
            border-radius:20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color:white;
        ">
            <h1>Find Your Dream Home 🏡</h1>
            <p>AI-powered property price prediction platform</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Get Started"):
            navigate("login")

    with col2:
        st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994")

    st.markdown("## ✨ Features")

    features = ["Price Prediction", "Budget Analyzer", "Location Pricing"]

    cols = st.columns(3)

    for i, f in enumerate(features):
        with cols[i]:
            st.info(f)

    st.markdown("## 🏡 Properties")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c")
        st.write("Villa")

    with col2:
        st.image("https://images.unsplash.com/photo-1599423300746-b62533397364")
        st.write("Apartment")

    with col3:
        st.image("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85")
        st.write("Studio")