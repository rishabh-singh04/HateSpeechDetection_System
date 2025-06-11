# frontend/app.py
import sys
from pathlib import Path
import streamlit as st

# Initialize session state first (this doesn't count as a Streamlit command)
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'notification' not in st.session_state:
    st.session_state.notification = None

# Set page config must be the first Streamlit command
from components.common import setup_page_config
setup_page_config()

# Then proceed with other imports and initialization
frontend_dir = str(Path(__file__).parent)
if frontend_dir not in sys.path:
    sys.path.append(frontend_dir)

from components.common import load_assets
from pages.login_register import show_auth_page

def main():
    load_assets()
    st.title("🛡️ Content Moderation Dashboard")
    st.markdown("---")
    
    if not st.session_state.get('access_token'):
        show_auth_page()
        st.stop()
    
    # Main application after authentication
    from components.auth import show_sidebar
    show_sidebar()
    
    
    
    # Show notification if exists
    if st.session_state.get('notification'):
        st.success(st.session_state.notification)
        del st.session_state.notification

if __name__ == "__main__":
    main()