import streamlit as st

from accounts import AccountError, authenticate


def show_login():
    st.title("🔐 Login")
    if st.session_state.pop("account_created", False):
        st.success("Account created! Please log in.")

    with st.form("login_form"):
        username = st.text_input("Username", max_chars=30)
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        try:
            authenticated_username = authenticate(username, password)
        except AccountError as exc:
            st.error(str(exc))
        else:
            st.session_state.logged_in = True
            st.session_state.username = authenticated_username
            if st.session_state.get("page") not in {"home", "predict", "profile"}:
                st.session_state.page = "home"
            st.switch_page("app.py")

    st.page_link("pages/register.py", label="Create Account")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.switch_page("app.py")


if __name__ == "__main__":
    show_login()
