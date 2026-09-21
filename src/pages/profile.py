import streamlit as st

from accounts import AccountError, update_account


def show_profile(navigate):
    if not st.session_state.get("logged_in") or not st.session_state.get("username"):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.session_state.page = "profile"
        st.switch_page("pages/login.py")
        return

    st.title("👤 Profile")
    if st.session_state.pop("profile_updated", False):
        st.success("Updated successfully")
    st.info(f"Username: {st.session_state.username}")

    with st.form("profile_form", clear_on_submit=True):
        new_username = st.text_input("New Username", max_chars=30)
        new_password = st.text_input("New Password", type="password")
        submitted = st.form_submit_button("Update")

    if submitted:
        try:
            username = update_account(st.session_state.username, new_username, new_password)
        except AccountError as exc:
            st.error(str(exc))
        else:
            # Only publish the new identity after the transaction has committed.
            st.session_state.username = username
            st.session_state.profile_updated = True
            st.rerun()

    if st.button("Back"):
        navigate("home")


if __name__ == "__main__":
    def navigate(page):
        st.session_state.page = page
        st.switch_page("app.py")

    show_profile(navigate)
