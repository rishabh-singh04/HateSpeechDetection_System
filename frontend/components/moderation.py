# # frontend/components/moderation.py
# import streamlit as st
# from components.common import api_request

# def render_text_moderation():
#     st.header("📝 Text Content Moderation")
    
#     with st.expander("ℹ️ About this feature", expanded=False):
#         st.info("""
#         This tool analyzes text content for potentially harmful or inappropriate material.
#         It uses advanced AI models to detect hate speech, harassment, and other policy violations.
#         """)
    
#     with st.form("text_moderation_form"):
#         text_input = st.text_area(
#             "Enter text to moderate:", 
#             height=200,
#             placeholder="Paste or type content here..."
#         )
        
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             submitted = st.form_submit_button("🚀 Analyze Content")
#         with col2:
#             if st.form_submit_button("📋 Clear", type="secondary"):
#                 st.rerun()
        
#         if submitted and text_input:
#             with st.spinner("🔍 Analyzing content..."):
#                 try:
#                     response = api_request(
#                         "POST",
#                         "moderation/text",  # Removed leading slash
#                         json={"text": text_input}
#                     )
                    
#                     if response:
#                         if response.status_code == 200:
#                             display_moderation_results(response.json())
#                         else:
#                             st.error(f"API Error: {response.status_code} - {response.text}")
#                     else:
#                         st.error("No response from server")
#                 except Exception as e:
#                     st.error(f"Request failed: {str(e)}")

# def display_moderation_results(result):
#     st.markdown("---")
#     st.subheader("📊 Moderation Results")
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("### 🏷️ Classification")
#         classification = result.get('classification', 'N/A')
#         emoji = "✅" if classification == "Safe" else "⚠️" if classification == "Warning" else "❌"
#         st.markdown(f"""
#         <div class='classification-box'>
#             <div style="font-size: 24px; margin-bottom: 10px;">{emoji}</div>
#             {classification}
#         </div>""", unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("### 📊 Confidence")
#         confidence = result.get('confidence', 0)
#         st.markdown(f"""
#         <div class='confidence-box'>
#             <div class="gauge" style="width: {confidence*100}%"></div>
#             {confidence:.2f}
#         </div>""", unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("### 🚦 Recommended Action")
#         action = result.get('action', 'N/A')
#         action_emoji = "👀" if "Review" in action else "✅" if "Approve" in action else "❌"
#         st.markdown(f"""
#         <div class='action-box'>
#             <div style="font-size: 24px; margin-bottom: 10px;">{action_emoji}</div>
#             {action}
#         </div>""", unsafe_allow_html=True)
    
#     if 'reasoning' in result:
#         st.markdown("### 🧠 Reasoning")
#         st.markdown(f"""
#         <div class='reasoning-box'>
#             {result['reasoning']}
#         </div>""", unsafe_allow_html=True)
    
#     st.caption(f"⏱️ Processed at: {result.get('timestamp', 'N/A')}")

# frontend/components/moderation.py
import streamlit as st
from components.common import api_request
from components.audio_recorder import audio_recorder_component

def render_text_moderation():
    st.header("📝 Content Moderation")
    
    with st.expander("ℹ️ About this feature", expanded=False):
        st.info("""
        This tool analyzes text content for potentially harmful or inappropriate material.
        It uses advanced AI models to detect hate speech, harassment, and other policy violations.
        """)
    
    # Audio recording section
    st.subheader("🎤 Audio Transcription")
    audio_recorder_component()
    
    # Text moderation section
    st.subheader("📝 Text Analysis")
    with st.form("text_moderation_form"):
        text_input = st.text_area(
            "Enter text to moderate:", 
            height=200,
            placeholder="Paste or type content here...",
            key="moderation_text_input"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("🚀 Analyze Content")
        with col2:
            if st.form_submit_button("📋 Clear", type="secondary"):
                st.session_state.moderation_text_input = ""
                st.rerun()
        
        if submitted and text_input:
            with st.spinner("🔍 Analyzing content..."):
                try:
                    response = api_request(
                        "POST",
                        "moderation/text",
                        json={"text": text_input}
                    )
                    
                    if response:
                        if response.status_code == 200:
                            display_moderation_results(response.json())
                        else:
                            st.error(f"API Error: {response.status_code} - {response.text}")
                    else:
                        st.error("No response from server")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")

def display_moderation_results(result):
    st.markdown("---")
    st.subheader("📊 Moderation Results")
    
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
    
    if 'reasoning' in result:
        st.markdown("### 🧠 Reasoning")
        st.markdown(f"""
        <div class='reasoning-box'>
            {result['reasoning']}
        </div>""", unsafe_allow_html=True)
    
    st.caption(f"⏱️ Processed at: {result.get('timestamp', 'N/A')}")