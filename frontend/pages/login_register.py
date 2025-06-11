# frontend/pages/login_register.py
import streamlit as st
from components.common import api_request

def show_auth_page():
    """Show login or register form based on user selection"""
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()

# frontend/pages/login_register.py

def show_login_form():
    """Display login form"""
    with st.form("login_form"):
        st.subheader("Login")
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # Prepare form-urlencoded data
            login_data = {
                "username": username_or_email,
                "password": password
            }
            
            try:
                response = api_request(
                    "POST",
                    "auth/login",
                    data=login_data,  # Changed from json to data
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response and response.status_code == 200:
                    st.session_state.access_token = response.json().get("access_token")
                    st.success("Logged in successfully!")
                    st.rerun()
                elif response:
                    st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Login error: {str(e)}")


def show_register_form():
    """Display registration form"""
    with st.form("register_form"):
        st.subheader("Create New Account")
        
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username*")
            email = st.text_input("Email*")
        with col2:
            full_name = st.text_input("Full Name (optional)")
            password = st.text_input("Password*", type="password")
        
        st.markdown("<small>* Required fields</small>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not username or not email or not password:
                st.warning("Please fill in all required fields")
                return
                
            response = api_request(
                "POST",
                "/users/",
                json={
                    "username": username,
                    "email": email,
                    "full_name": full_name,
                    "password": password
                }
            )
            
            if response and response.status_code == 200:
                st.success("Account created successfully! Please login.")
                st.session_state.notification = "Account created successfully!"
                st.rerun()