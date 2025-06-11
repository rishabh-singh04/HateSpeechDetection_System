# frontend/components/auth.py
import streamlit as st
from components.common import api_request
from components.moderation import render_text_moderation
from components.policy import render_policy_search
from components.user_management import render_user_management

def show_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.title("🚀 Navigation")
        st.markdown("---")
        app_mode = st.radio(
            "Choose a feature:",
            ["Text Moderation", "Policy Search", "User Management"]
        )
        
        st.markdown("---")
        if st.button("🔒 Logout"):
            logout()
        
        st.markdown("### 👤 User Info")
        st.markdown("""
        <div class="user-info">
            <p><strong>Role:</strong> Moderator</p>
            <p><strong>Last Active:</strong> Just now</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Render the selected page
    if app_mode == "Text Moderation":
        render_text_moderation()
    elif app_mode == "Policy Search":
        render_policy_search()
    elif app_mode == "User Management":
        render_user_management()

def logout():
    """Logout the current user"""
    st.session_state.access_token = None
    st.success("Logged out successfully!")
    st.rerun()