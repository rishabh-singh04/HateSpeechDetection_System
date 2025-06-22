# frontend/components/user_management.py

import streamlit as st
from components.common import api_request
import time

def render_user_management():
    """Render the user management page to list users and perform actions."""
    st.header("👥 User Management")
    
    # Use session state to track deletion status
    if 'deleted_users' not in st.session_state:
        st.session_state.deleted_users = set()
    
    users = _fetch_users()
    if users is None:
        st.warning("No users found or failed to load users.")
        return

    # Filter out deleted users
    active_users = [user for user in users if user.get('id') not in st.session_state.deleted_users]
    
    for user in active_users:
        _render_user_card(user)

def _fetch_users():
    """Fetch user list from backend API"""
    try:
        response = api_request("GET", "users")
        if response and response.status_code == 200:
            return response.json()
        st.error(f"Failed to load users. Status code: {response.status_code if response else 'No response'}")
        return None
    except Exception as e:
        st.error(f"Error fetching users: {str(e)}")
        return None

def _render_user_card(user: dict):
    user_id = user.get('id')
    if user_id is None:
        st.error("User data missing ID field")
        return

    username = user.get('username') or user.get('email') or 'Unknown User'
    role = "Admin" if user.get('is_superuser', False) else "User"
    last_active = user.get('last_active', 'N/A')

    with st.container():
        st.markdown(f"""
        <div class="user-card" style="
            background: var(--card-bg);
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #9c27b0;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        ">
            <strong>{username}</strong><br>
            Role: {role}<br>
            Last Active: {last_active}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        
        with col1:
            delete_key = f"delete_{user_id}"
            if st.button(f"Delete {username}", key=delete_key):
                st.session_state[f'delete_confirm_{user_id}'] = True
                
        with col2:
            if st.button(f"Reset Password {username}", key=f"reset_{user_id}"):
                st.warning("Password reset functionality not implemented yet.")
        
        # Show confirmation only if delete button was clicked for this user
        if st.session_state.get(f'delete_confirm_{user_id}', False):
            if _confirm_delete(user_id, username):
                if _delete_user(user_id, username):
                    # Mark user as deleted and force rerun
                    st.session_state.deleted_users.add(user_id)
                    st.session_state[f'delete_confirm_{user_id}'] = False
                    st.rerun()

def _confirm_delete(user_id: int, username: str) -> bool:
    """Show confirmation dialog for delete action."""
    st.warning(f"Are you sure you want to permanently delete user {username}?")
    confirm_col, cancel_col = st.columns([1, 1])
    
    with confirm_col:
        if st.button("Yes, delete permanently", key=f"confirm_delete_{user_id}"):
            return True
            
    with cancel_col:
        if st.button("Cancel", key=f"cancel_delete_{user_id}"):
            st.session_state[f'delete_confirm_{user_id}'] = False
            st.rerun()
    return False

def _delete_user(user_id: int, username: str) -> bool:
    """Send delete request to backend for the given user."""
    try:
        with st.spinner(f"Deleting user {username}..."):
            response = api_request("DELETE", f"users/{user_id}")
            
            if response is None:
                st.error("No response from server")
                return False
                
            if response.status_code in [200, 204]:
                st.success(f"User {username} deleted successfully.")
                return True
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"Failed to delete user: {error_detail}")
                return False
    except Exception as e:
        st.error(f"Error deleting user: {str(e)}")
        return False