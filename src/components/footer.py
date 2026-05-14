import streamlit as st

def render_footer():
    st.markdown("""
    <hr>
    <div style="text-align:center;color:gray;">
        © 2026 House Price Predictor | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)