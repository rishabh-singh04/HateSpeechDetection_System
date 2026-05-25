import streamlit as st
from components.common import setup_page_config, load_assets
from components.auth import check_auth, show_sidebar
from pages.login_register import show_auth_page
from components.navbar import render_navbar

def main():
    # Global page setup
    setup_page_config()
    load_assets()

    # Check user login
    if not check_auth():
        show_auth_page()
    else:
        # Main heading at the absolute top with no spacing
        st.markdown("""
        <div style="margin-top: -1rem;">
            <h1 class='content-moderation-header'>
                🛡️ Content Moderation Dashboard
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        render_navbar()
        show_sidebar()

        # Welcome message below
        st.markdown("""
        <div style="margin-top: -1rem;">
            <p style='font-size: 1.1rem; color: var(--text-secondary);'>
                Use the sidebar to navigate between moderation, policy search, and user management features.
            </p>
            <hr style='margin-bottom: 2rem;' />
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    