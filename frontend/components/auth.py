# frontend/components/auth.py

import streamlit as st
from streamlit.components.v1 import html
from components.common import api_request

def check_auth():
    """Check if user is authenticated"""
    return st.session_state.get('access_token') is not None

def logout():
    """Logout the current user"""
    try:
        api_request("POST", "auth/logout")
    except Exception:
        pass

    for key in ['access_token', 'username']:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("Logged out successfully!")
    st.rerun()

def show_sidebar():
    """Render the simplified sidebar navigation"""
    if not check_auth():
        return

    with st.sidebar:
        st.title(f"👋 Welcome, {st.session_state.get('username', 'User')}")
        st.markdown("---")

        # Theme toggle radio
        theme = st.radio(
            "Theme",
            ["🌙 Dark", "☀️ Light"],
            index=0 if st.session_state.get('theme', 'light-mode') == 'dark-mode' else 1,
            horizontal=True,
            key="theme_toggle"
        )

        # Theme logic and messaging
        theme_value = 'dark-mode' if theme == "🌙 Dark" else 'light-mode'
        if st.session_state.get('theme') != theme_value:
            st.session_state.theme = theme_value
            js = f"""
            <script>
            window.postMessage({{
                type: 'setTheme',
                theme: '{theme_value}'
            }}, '*');
            </script>
            """
            html(js)

        st.markdown("---")

        app_mode = st.radio(
            "Navigation",
            ["Moderation", "Policy Documents", "User Management"],  # Changed from "Policy Search"
            key="app_mode"
        )

        st.markdown("---")
        if st.button("🔒 Logout"):
            logout()

    # Route page rendering
    if st.session_state.app_mode == "Moderation":
        from components.moderation import render_text_moderation
        render_text_moderation()
    elif st.session_state.app_mode == "Policy Documents":  # Changed from "Policy Search"
        from components.policy import render_policy_documents  # Changed import
        render_policy_documents()  # Changed function call
    elif st.session_state.app_mode == "User Management":
        from components.user_management import render_user_management
        render_user_management()