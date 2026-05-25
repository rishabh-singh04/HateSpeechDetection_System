# frontend/pages/login_register.py

import streamlit as st
from components.common import api_request

def show_auth_page():
    """Entry point to render login/register page."""
    render_login_register()

def render_login_register():
    """Render login and registration forms with tab switching."""
    st.title("🔐 Login / Register")

    # Initialize session state
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = "Login"

    tab = st.radio(
        "Select Mode",
        ["Login", "Register"],
        horizontal=True,
        index=0 if st.session_state.auth_tab == "Login" else 1,
        key="auth_tab_radio"
    )

    st.session_state.auth_tab = tab  # Sync state on change

    if tab == "Login":
        _render_login_form()
    else:
        _render_register_form()

def _render_login_form():
    with st.form(key="login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        submitted = st.form_submit_button("🔑 Login")
        if submitted:
            if not username or not password:
                st.error("Please enter both username and password")
                return
            _login_user(username, password)

def _render_register_form():
    with st.form(key="register_form"):
        email = st.text_input("Email", key="register_email")
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")

        submitted = st.form_submit_button("📝 Register")
        if submitted:
            if not (email and username and password and password_confirm):
                st.error("All fields are required")
                return
            if password != password_confirm:
                st.error("Passwords do not match")
                return
            _register_user(email, username, password)

def _login_user(username, password):
    try:
        response = api_request(
            "POST",
            "auth/login",
            data={
                "username": username,
                "password": password,
                "grant_type": "password"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response and response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user = data.get("username", username)

            if token:
                st.session_state.access_token = token
                st.session_state.username = user
                st.success(f"✅ Welcome back, {user}!")
                st.experimental_rerun()
            else:
                st.error("Login failed: No access token received.")
        else:
            error_msg = response.json().get("detail", "Login failed") if response else "No response from server"
            st.error(f"❌ Login failed: {error_msg}")
    except Exception as e:
        st.error(f"⚠️ Login request error: {str(e)}")

def _register_user(email, username, password):
    try:
        response = api_request(
            "POST",
            "auth/register",
            json={
                "email": email,
                "username": username,
                "password": password
            }
        )
        if response and response.status_code in [200, 201]:  # Accept both 200 and 201
            response_data = response.json()
            if response_data.get("success", False):  # Check for success flag in response
                st.success("🎉 Registration successful! Please log in.")
                # Clear the form fields
                for key in [
                    "register_email",
                    "register_username",
                    "register_password",
                    "register_password_confirm"
                ]:
                    st.session_state[key] = ""
                st.session_state.auth_tab = "Login"
                st.rerun()
            else:
                error_msg = response_data.get("detail", "Registration failed")
                st.error(f"❌ Registration failed: {error_msg}")
        else:
            error_msg = response.json().get("detail", "Registration failed") if response else "No response from server"
            st.error(f"❌ Registration failed: {error_msg}")
    except Exception as e:
        st.error(f"⚠️ Registration request error: {str(e)}")