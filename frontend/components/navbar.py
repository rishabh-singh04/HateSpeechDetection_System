# frontend/components/navbar.py
import streamlit as st
from streamlit.components.v1 import html

def render_navbar():
    """Render a consistent navigation bar with theme toggle"""
    if not st.session_state.get('access_token'):
        return

    st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        right: 0;
        width: 100%;
        background: transparent;
        padding: 1rem;
        display: flex;
        justify-content: flex-end;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

    theme_value = st.session_state.get('theme', 'dark-mode')
    theme_checked = 'checked' if theme_value == 'light-mode' else ''

    html(f"""
    <div class="navbar">
        <label class="switch">
            <input type="checkbox" id="themeToggle" {theme_checked}>
            <span class="slider round"></span>
        </label>
    </div>

    <script>
    document.getElementById('themeToggle').addEventListener('change', function(e) {{
        const theme = e.target.checked ? 'light-mode' : 'dark-mode';
        window.postMessage({{
            type: 'setTheme',
            theme: theme
        }}, '*');
    }});
    </script>

    <style>
    .switch {{
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }}
    .switch input {{ opacity: 0; width: 0; height: 0; }}
    .slider {{
        position: absolute;
        cursor: pointer;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: #6b4b2a;
        transition: .4s;
        border-radius: 34px;
    }}
    .slider:before {{
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
    }}
    input:checked + .slider {{
        background-color: #8a6d3b;
    }}
    input:checked + .slider:before {{
        transform: translateX(26px);
    }}
    </style>
    """, height=0)
