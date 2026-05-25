import os
import streamlit as st
import requests
from streamlit.components.v1 import html

BASE_URL = "http://localhost:8000/api"

def setup_page_config():
    st.set_page_config(
        page_title="Content Moderation Dashboard",
        page_icon=":shield:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_assets():
    """Load CSS and enhanced JS for theme and UI."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.dirname(current_dir)
    css_file = os.path.join(frontend_dir, 'assets', 'styles.css')

    # Theme JS
    theme_js = """
    <script>
    function setTheme(theme) {
        document.body.classList.remove('dark-mode', 'light-mode');
        document.body.classList.add(theme);
        document.body.setAttribute("data-theme", theme);
        localStorage.setItem('theme', theme);
    }

    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light-mode';
        setTheme(savedTheme);
        window.parent.postMessage({ type: 'streamlit:setTheme', theme: savedTheme }, '*');
    }

    window.addEventListener('message', (event) => {
        if (event.data.type === 'setTheme') {
            setTheme(event.data.theme);
        }
    });

    document.addEventListener("DOMContentLoaded", initTheme);
    </script>
    """
    html(theme_js)

    # Load style.css
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at: {css_file}")
        st.markdown("<style>body { font-family: Arial, sans-serif; }</style>", unsafe_allow_html=True)

    # UI enhancements (hover, button scale)
    ui_js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.stExpander');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.02)';
                this.style.transition = 'transform 0.3s ease';
            });
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });

        const buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            });
        });
    });
    </script>
    """
    html(ui_js)

def api_request(method, endpoint, **kwargs):
    """Make authenticated API requests to backend."""
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]

    headers = kwargs.pop('headers', {})
    token = st.session_state.get('access_token')
    if token:
        headers['Authorization'] = f"Bearer {token}"

    try:
        response = requests.request(
            method,
            f"{BASE_URL}/{endpoint}",
            headers=headers,
            **kwargs
        )
        
        if response.status_code == 401:
            st.error("Session expired. Please login again.")
            st.session_state.pop('access_token', None)
            st.rerun()

        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None
