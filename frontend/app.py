# app/ui/streamlit_app.py

import streamlit as st
import requests
import time
from io import BytesIO
from streamlit.components.v1 import html
from typing import Optional

# Custom CSS and JS for enhanced interactivity
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_js():
    # JavaScript for additional interactivity
    js = """
    <script>
    // Add hover effects to cards
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
        
        // Add click animation to buttons
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

# API Endpoints
BASE_URL = "http://localhost:8000/api/routes"
MODERATE_TEXT_ENDPOINT = f"{BASE_URL}/moderation/text"
SEARCH_POLICIES_ENDPOINT = f"{BASE_URL}/policies/search"
LIST_POLICIES_ENDPOINT = f"{BASE_URL}/policies/"
CREATE_USER_ENDPOINT = f"{BASE_URL}/users/"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"

def check_authentication():
    """Check if user is authenticated"""
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    return st.session_state.access_token is not None

def login_form():
    """Render login form"""
    with st.form("login_form"):
        st.subheader("Login")
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            try:
                # Determine if input is email or username
                login_data = {
                    "username": username_or_email,
                    "password": password
                } if "@" not in username_or_email else {
                    "username": username_or_email,  # OAuth2PasswordRequestForm expects 'username' field
                    "password": password
                }
                
                response = requests.post(
                    f"{BASE_URL}/auth/login",
                    data=login_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code == 200:
                    st.session_state.access_token = response.json().get("access_token")
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

def logout():
    """Logout user"""
    st.session_state.access_token = None
    st.success("Logged out successfully!")
    st.experimental_rerun()

def main():
    st.set_page_config(
        page_title="Content Moderation Dashboard",
        page_icon=":shield:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS and JS
    local_css("frontend/styles.css")
    load_js()
    
    # Authentication check
    if not check_authentication():
        login_form()
        st.stop()
    
    # Sidebar with user info
    with st.sidebar:
        st.title("🚀 Navigation")
        st.markdown("---")
        app_mode = st.radio("Choose a feature:", 
                          ["Text Moderation", "Policy Search", "User Management"])
        
        st.markdown("---")
        if st.button("🔒 Logout"):
            logout()
        
        # User info section
        st.markdown("### 👤 User Info")
        st.markdown("""
        <div class="user-info">
            <p><strong>Role:</strong> Moderator</p>
            <p><strong>Last Active:</strong> Just now</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.title("🛡️ Content Moderation Dashboard")
    st.markdown("---")
    
    # Notification area
    with st.empty():
        if st.session_state.get('notification'):
            st.success(st.session_state.notification)
            time.sleep(3)
            st.session_state.notification = None
    
    if app_mode == "Text Moderation":
        render_text_moderation()
    elif app_mode == "Policy Search":
        render_policy_search()
    elif app_mode == "User Management":
        render_user_management()

def render_text_moderation():
    st.header("📝 Text Content Moderation")
    
    with st.expander("ℹ️ About this feature", expanded=False):
        st.info("""
        This tool analyzes text content for potentially harmful or inappropriate material.
        It uses advanced AI models to detect hate speech, harassment, and other policy violations.
        """)
    
    with st.form("text_moderation_form"):
        text_input = st.text_area("Enter text to moderate:", height=200,
                                placeholder="Paste or type content here...",
                                help="Content will be analyzed in real-time")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("🚀 Analyze Content", 
                                            use_container_width=True)
        with col2:
            if st.form_submit_button("📋 Clear", 
                                   use_container_width=True,
                                   type="secondary"):
                st.experimental_rerun()
        
        if submitted and text_input:
            with st.spinner("🔍 Analyzing content..."):
                try:
                    response = requests.post(
                        MODERATE_TEXT_ENDPOINT,
                        json={"text": text_input},
                        headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        display_moderation_results(result)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"API request failed: {str(e)}")

def render_policy_search():
    st.header("🔍 Policy Document Search")
    
    with st.expander("ℹ️ Search tips", expanded=False):
        st.info("""
        - Use quotes for exact phrases: "content policy"
        - Combine terms: moderation AND guidelines
        - Exclude terms: policy NOT update
        """)
    
    with st.form("policy_search_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search policies:", 
                                       placeholder="Enter search terms...",
                                       help="Use advanced search operators for better results")
        with col2:
            limit = st.number_input("Results limit:", min_value=1, max_value=20, value=5)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("🔍 Search", 
                                           use_container_width=True)
        with col2:
            if st.form_submit_button("🔄 Reset", 
                                   use_container_width=True,
                                   type="secondary"):
                st.experimental_rerun()
        
        if submitted and search_query:
            with st.spinner("Searching policies..."):
                try:
                    response = requests.get(
                        SEARCH_POLICIES_ENDPOINT,
                        params={"query": search_query, "limit": limit},
                        headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        display_search_results(results)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"API request failed: {str(e)}")

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
            
            submitted = st.form_submit_button("✨ Create User", 
                                            use_container_width=True)
            
            if submitted:
                if not username or not email or not password:
                    st.warning("Please fill in all required fields")
                    return
                    
                with st.spinner("Creating user..."):
                    try:
                        response = requests.post(
                            CREATE_USER_ENDPOINT,
                            json={
                                "username": username,
                                "email": email,
                                "full_name": full_name,
                                "password": password
                            },
                            headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                        )
                        
                        if response.status_code == 200:
                            user = response.json()
                            st.session_state.notification = f"User {user['username']} created successfully!"
                            st.experimental_rerun()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    
                    except Exception as e:
                        st.error(f"API request failed: {str(e)}")
    
    with tab2:
        st.subheader("👥 All Users")
        with st.spinner("Loading users..."):
            try:
                response = requests.get(
                    f"{BASE_URL}/users/",
                    headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                )
                
                if response.status_code == 200:
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
                                        # Implement delete functionality
                                        pass
                    else:
                        st.info("No users found")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"API request failed: {str(e)}")

def display_moderation_results(result):
    st.markdown("---")
    st.subheader("📊 Moderation Results")
    
    # Classification and action
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🏷️ Classification")
        classification = result.get('classification', 'N/A')
        emoji = "✅" if classification == "Safe" else "⚠️" if classification == "Warning" else "❌"
        st.markdown(f"""
        <div class='classification-box'>
            <div style="font-size: 24px; margin-bottom: 10px;">{emoji}</div>
            {classification}
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Confidence")
        confidence = result.get('confidence', 0)
        st.markdown(f"""
        <div class='confidence-box'>
            <div class="gauge" style="width: {confidence*100}%"></div>
            {confidence:.2f}
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🚦 Recommended Action")
        action = result.get('action', 'N/A')
        action_emoji = "👀" if "Review" in action else "✅" if "Approve" in action else "❌"
        st.markdown(f"""
        <div class='action-box'>
            <div style="font-size: 24px; margin-bottom: 10px;">{action_emoji}</div>
            {action}
        </div>""", unsafe_allow_html=True)
    
    # Reasoning
    if 'reasoning' in result:
        st.markdown("### 🧠 Reasoning")
        st.markdown(f"""
        <div class='reasoning-box'>
            {result['reasoning']}
        </div>""", unsafe_allow_html=True)
    
    # Timestamp
    st.caption(f"⏱️ Processed at: {result.get('timestamp', 'N/A')}")

def display_search_results(results):
    st.markdown("---")
    
    if not results.get('results'):
        st.warning("No matching policies found")
        return
    
    st.subheader(f"🔍 Search Results (took {results.get('search_time_ms', 0):.2f} ms)")
    
    for policy in results['results']:
        with st.expander(f"📄 {policy.get('name', 'Unnamed Policy')} (Score: {policy.get('score', 0):.2f})"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**ID:** {policy.get('id')}")
                st.markdown(f"**Content:**")
                st.markdown(f"<div class='policy-content'>{policy.get('content', 'No content')}</div>", 
                           unsafe_allow_html=True)
            with col2:
                if policy.get('score') is not None:
                    st.markdown("**Relevance:**")
                    st.progress(min(policy['score'], 1.0))
                
                if st.button("📋 Copy", key=f"copy_{policy.get('id')}"):
                    st.session_state.notification = "Policy content copied to clipboard!"
                    st.experimental_rerun()

if __name__ == "__main__":
    main()