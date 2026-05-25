# frontend/components/policy.py

import streamlit as st
from components.common import api_request
from datetime import datetime

def render_policy_documents():
    """Display all policy documents in an organized way."""
    st.header("📜 Policy Documents", anchor="policy-docs")
    
    with st.expander("ℹ️ About Policy Documents", expanded=False):
        st.info(
            "These are the official content moderation policies that govern "
            "what content is allowed on our platform."
        )
    
    # Fetch and display policy documents
    with st.spinner("Loading policy documents..."):
        response = api_request("GET", "policies/")
        if response and response.status_code == 200:
            policies = response.json()
            _display_policy_documents(policies)
        else:
            st.error("Failed to load policy documents")

def _display_policy_documents(policies):
    """Display policy documents with categorized sections."""
    if not policies:
        st.warning("No policy documents available")
        return
    
    # Group by categories if available, otherwise show all
    categories = {p.get('category', 'General') for p in policies}
    
    for category in sorted(categories):
        category_policies = [p for p in policies if p.get('category', 'General') == category]
        
        with st.expander(f"📂 {category}", expanded=True):
            for policy in category_policies:
                _display_policy_card(policy)

def _display_policy_card(policy):
    """Display individual policy document card with colored border."""
    # Determine border color based on policy type/status
    border_color = {
        'General': '#1976d2',  # Blue
        'Security': '#2e7d32',  # Green
        'Legal': '#d32f2f',    # Red
        'Community': '#f57c00'  # Orange
    }.get(policy.get('category', 'General'), '#1976d2')  # Default to blue
    
    with st.container():
        st.markdown(f"""
        <div class="policy-card" style="
            background: var(--card-bg);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid {border_color};
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.15);
        ">
            <h3 style="margin-top: 0; color: var(--primary);">{policy.get('name', 'Unnamed Policy')}</h3>
            <div class="snippet-box" style="
                background: rgba(0,0,0,0.1);
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
            ">
                {policy.get('content', 'No content available')}
            </div>
        </div>
        """, unsafe_allow_html=True)