# frontend/components/common.py

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
    """Load CSS and JS assets"""
    # Get the absolute path to the assets directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.dirname(current_dir)
    css_file = os.path.join(frontend_dir, 'assets', 'styles.css')
    
    # print(f"Correct CSS path: {css_file}")  # Debugging
    
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at: {css_file}")
        # Fallback to inline CSS
        st.markdown("""
        <style>
        /* Basic fallback styles */
        body { font-family: Arial, sans-serif; }
        </style>
        """, unsafe_allow_html=True)
    
    # JS
    js = """
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
    html(js)

def api_request(method, endpoint, **kwargs):
    """Helper function for API requests"""
    # Ensure endpoint doesn't start with slash to avoid double slashes
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    
    headers = kwargs.pop('headers', {})
    if 'access_token' in st.session_state:
        headers['Authorization'] = f"Bearer {st.session_state.access_token}"
    
    try:
        response = requests.request(
            method, 
            f"{BASE_URL}/{endpoint}",  # Now properly formats to /api/endpoint
            headers=headers, 
            **kwargs
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None