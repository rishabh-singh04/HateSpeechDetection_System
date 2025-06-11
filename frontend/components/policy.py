# frontend/components/policy.py

import streamlit as st
from components.common import api_request

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
            search_query = st.text_input(
                "Search policies:", 
                placeholder="Enter search terms..."
            )
        with col2:
            limit = st.number_input("Results limit:", min_value=1, max_value=20, value=5)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("🔍 Search")
        with col2:
            if st.form_submit_button("🔄 Reset"):
                st.rerun()
    
    # Display results outside the form to allow buttons
    if submitted and search_query:
        with st.spinner("Searching policies..."):
            response = api_request(
                "GET",
                "policies/search",
                params={"query": search_query, "limit": limit}
            )
            
            if response and response.status_code == 200:
                display_search_results(response.json())

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
                
                # Button is now safely outside the form
                if st.button("📋 Copy", key=f"copy_{policy.get('id')}"):
                    st.session_state.notification = "Policy content copied to clipboard!"
                    st.experimental_rerun()