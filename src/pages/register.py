import streamlit as st

from accounts import AccountError, register_account


def show_register():
    st.title("📝 Register")
    with st.form("register_form"):
        username = st.text_input("Username", max_chars=30)
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

    if submitted:
        try:
            register_account(username, password)
        except AccountError as exc:
            st.error(str(exc))
        else:
            st.session_state.account_created = True
            st.switch_page("pages/login.py")

    st.page_link("pages/login.py", label="Already have an account? Log in")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.switch_page("app.py")


if __name__ == "__main__":
    show_register()
