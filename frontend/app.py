# app/ui/streamlit_app.py

import streamlit as st
import requests
import time
from io import BytesIO

# Custom CSS for dark theme with brown/yellow gradient
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# API Endpoints - Updated to match your routes
BASE_URL = "http://localhost:8000/api/routes"
MODERATE_TEXT_ENDPOINT = f"{BASE_URL}/moderation/text"
SEARCH_POLICIES_ENDPOINT = f"{BASE_URL}/policies/search"
LIST_POLICIES_ENDPOINT = f"{BASE_URL}/policies/"
CREATE_USER_ENDPOINT = f"{BASE_URL}/users/"

def main():
    st.set_page_config(
        page_title="Content Moderation Dashboard",
        page_icon=":shield:",
        layout="wide"
    )
    
    # Load custom CSS
    local_css("frontend/styles.css")
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.markdown("---")
        app_mode = st.radio("Choose a feature:", 
                          ["Text Moderation", "Policy Search", "User Management"])
    
    # Main content
    st.title(":shield: Content Moderation Dashboard")
    st.markdown("---")
    
    if app_mode == "Text Moderation":
        render_text_moderation()
    elif app_mode == "Policy Search":
        render_policy_search()
    elif app_mode == "User Management":
        render_user_management()

def render_text_moderation():
    st.header("Text Content Moderation")
    
    with st.form("text_moderation_form"):
        text_input = st.text_area("Enter text to moderate:", height=150,
                                placeholder="Paste or type content here...")
        
        submitted = st.form_submit_button("Analyze Content")
        
        if submitted and text_input:
            with st.spinner("Analyzing content..."):
                try:
                    response = requests.post(
                        MODERATE_TEXT_ENDPOINT,
                        json={"text": text_input}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        display_moderation_results(result)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"API request failed: {str(e)}")

def render_policy_search():
    st.header("Policy Document Search")
    
    with st.form("policy_search_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search policies:", 
                                       placeholder="Enter search terms...")
        with col2:
            limit = st.number_input("Results limit:", min_value=1, max_value=20, value=5)
        
        submitted = st.form_submit_button("Search")
        
        if submitted and search_query:
            with st.spinner("Searching policies..."):
                try:
                    response = requests.get(
                        SEARCH_POLICIES_ENDPOINT,
                        params={"query": search_query, "limit": limit}
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        display_search_results(results)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"API request failed: {str(e)}")

def render_user_management():
    st.header("User Management")
    
    with st.form("user_creation_form"):
        st.subheader("Create New User")
        username = st.text_input("Username")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name (optional)")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Create User")
        
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
                        }
                    )
                    
                    if response.status_code == 200:
                        user = response.json()
                        st.success(f"User {user['username']} created successfully!")
                        st.json(user)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"API request failed: {str(e)}")

def display_moderation_results(result):
    st.markdown("---")
    st.subheader("Moderation Results")
    
    # Classification and action
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Classification")
        st.markdown(f"<div class='classification-box'>{result.get('classification', 'N/A')}</div>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Confidence")
        confidence = result.get('confidence', 0)
        st.markdown(f"<div class='confidence-box'>{confidence:.2f}</div>",
                  unsafe_allow_html=True)
    
    with col3:
        st.markdown("### Recommended Action")
        st.markdown(f"<div class='action-box'>{result.get('action', 'N/A')}</div>", 
                   unsafe_allow_html=True)
    
    # Reasoning
    if 'reasoning' in result:
        st.markdown("### Reasoning")
        st.markdown(f"<div class='reasoning-box'>{result['reasoning']}</div>", 
                   unsafe_allow_html=True)
    
    # Timestamp
    st.caption(f"Processed at: {result.get('timestamp', 'N/A')}")

def display_search_results(results):
    st.markdown("---")
    
    if not results.get('results'):
        st.warning("No matching policies found")
        return
    
    st.subheader(f"Search Results (took {results.get('search_time_ms', 0):.2f} ms)")
    
    for policy in results['results']:
        with st.expander(f"📄 {policy.get('name', 'Unnamed Policy')} (Score: {policy.get('score', 0):.2f})"):
            st.markdown(f"**ID:** {policy.get('id')}")
            st.markdown(f"**Content:** {policy.get('content', 'No content')}")
            if policy.get('score') is not None:
                st.progress(min(policy['score'], 1.0))

if __name__ == "__main__":
    main()