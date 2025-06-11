# frontend/components/user_management.py
import streamlit as st
from components.common import api_request

def render_user_management():
    st.header("👥 User Management")
    
    tab1, tab2 = st.tabs(["Create User", "User List"])
    
    with tab1:
        with st.form("user_creation_form"):
            st.subheader("➕ Create New User")
            
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username*")
                email = st.text_input("Email*")
            with col2:
                full_name = st.text_input("Full Name (optional)")
                password = st.text_input("Password*", type="password")
            
            st.markdown("<small>* Required fields</small>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("✨ Create User")
            
            if submitted:
                if not username or not email or not password:
                    st.warning("Please fill in all required fields")
                    return
                    
                with st.spinner("Creating user..."):
                    response = api_request(
                        "POST",
                        "/users",  # Removed trailing slash for consistency
                        json={
                            "username": username,
                            "email": email,
                            "full_name": full_name,
                            "password": password
                        }
                    )
                    
                    if response and response.status_code == 200:
                        user = response.json()
                        st.session_state.notification = f"User {user['username']} created successfully!"
                        st.rerun()
                    elif response:
                        st.error(f"Failed to create user: {response.json().get('detail', 'Unknown error')}")
    
    with tab2:
        st.subheader("👥 All Users")
        with st.spinner("Loading users..."):
            response = api_request("GET", "/users")  # Removed trailing slash
            
            if response and response.status_code == 200:
                users = response.json()
                if users:
                    for user in users:
                        with st.expander(f"👤 {user['username']}"):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**Email:** {user['email']}")
                                st.markdown(f"**Full Name:** {user.get('full_name', 'N/A')}")
                                st.markdown(f"**Created:** {user['created_at']}")
                            with col2:
                                if st.button("🗑️ Delete", key=f"delete_{user['id']}"):
                                    delete_response = api_request("DELETE", f"/users/{user['id']}")
                                    if delete_response and delete_response.status_code == 200:
                                        st.session_state.notification = f"User {user['username']} deleted successfully!"
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to delete user: {delete_response.json().get('detail', 'Unknown error')}")
                else:
                    st.info("No users found")
            else:
                st.error(f"Failed to load users: {response.json().get('detail', 'Unknown error') if response else 'No response from server'}")