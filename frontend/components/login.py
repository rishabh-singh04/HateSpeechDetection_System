# frontend/components/login.py
import streamlit as st
from components.common import api_request

def login_form():
    """Render login form and handle authentication"""
    with st.form(key="login_form"):
        st.subheader("🔐 Login")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not username or not password:
                st.error("Please enter both username and password")
                return False
            
            with st.spinner("Authenticating..."):
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
                        st.session_state.access_token = data.get("access_token")
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                        return True
                    else:
                        error_detail = response.json().get("detail", "Unknown error") if response else "No response from server"
                        st.error(f"Login failed: {error_detail}")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
            return False
    return False