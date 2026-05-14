import streamlit as st

def render_header():
    st.markdown("""
    <div style="padding:15px;background:#111827;color:white;border-radius:10px;">
        <h2>🏠 House Price Predictor</h2>
    </div>
    """, unsafe_allow_html=True)