# frontend/components/moderation.py
import streamlit as st
from components.common import api_request
from components.audio_recorder import audio_recorder_component

def render_text_moderation():
    """Content moderation page with audio upload and transcription integration."""
    st.header("📝 Content Moderation")

    with st.expander("ℹ️ About this feature", expanded=False):
        st.info(
            "This tool analyzes text content for potentially harmful or inappropriate material. "
            "It uses advanced AI models to detect hate speech, harassment, and other policy violations."
        )

    # Audio upload and transcription section
    st.subheader("🎤 Audio Upload & Transcription")
    transcription_result = audio_recorder_component()

    # Update text input area with transcription if available and changed
    if transcription_result and 'text' in transcription_result:
        new_text = transcription_result['text']
        if st.session_state.get('moderation_text_input') != new_text:
            st.session_state.moderation_text_input = new_text

    _render_text_analysis_form()

def _render_text_analysis_form():
    """Render the moderation text input form with analyze and clear buttons."""
    with st.form(key="text_moderation_form"):
        text_input = st.text_area(
            "Enter text to moderate:",
            height=200,
            placeholder="Paste or type content here...",
            key="moderation_text_input",
            value=st.session_state.get("moderation_text_input", ""),
            help="Type or paste text, or upload audio to transcribe"
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button(
                "🚀 Analyze Content",
                help="Analyze the text for harmful content",
                type="primary"
            )
        with col2:
            if st.form_submit_button(
                "📋 Clear",
                help="Clear all text input",
                type="secondary"
            ):
                st.session_state.moderation_text_input = ""
                st.experimental_rerun()

        if submitted and text_input:
            _analyze_content(text_input)

def _analyze_content(text_input: str):
    """Call backend API for moderation analysis and display results."""
    with st.spinner("🔍 Analyzing content..."):
        try:
            response = api_request(
                "POST",
                "moderation/text",
                json={"text": text_input}
            )
            if response and response.status_code == 200:
                _display_moderation_results(response.json())
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response else 'No response from server'
                st.error(f"⚠️ Analysis failed: {error_detail}")
                st.warning("Using simplified analysis due to API issues...")
                _display_fallback_analysis(text_input)
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
            st.warning("Using simplified analysis due to API issues...")
            _display_fallback_analysis(text_input)

def _display_fallback_analysis(text_input: str):
    """Basic fallback analysis on client-side if API fails."""
    with st.container(border=True):
        st.subheader("⚠️ Basic Analysis Results", divider="orange")
        
        flagged_words = ["hate", "violence", "abuse", "attack"]
        found_words = [word for word in flagged_words if word in text_input.lower()]

        if found_words:
            st.warning(f"Found potentially concerning words: {', '.join(found_words)}")
        else:
            st.success("No obvious concerning content found")

        st.info("Note: Full analysis is currently unavailable. Contact support if this persists.")

def _display_moderation_results(result: dict):
    """Display detailed moderation results from backend with enhanced styling."""
    st.subheader("📊 Moderation Analysis Results", divider="blue")
    
    # Classification Summary
    classification = result.get('classification', 'Neutral').capitalize()
    confidence = result.get('confidence', 0)
    
    # Determine styling based on classification
    classification_style = {
        "neutral": {"color": "#2e7d32", "emoji": "✅", "label": "Neutral"},
        "review": {"color": "#ff9800", "emoji": "👀", "label": "Needs Review"},
        "hate": {"color": "#d32f2f", "emoji": "❌", "label": "Hate Speech"},
        "toxic": {"color": "#ff5722", "emoji": "☣️", "label": "Toxic"},
        "offensive": {"color": "#ffc107", "emoji": "⚠️", "label": "Offensive"}
    }.get(classification.lower(), {"color": "#2196f3", "emoji": "❓", "label": classification})

    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{classification_style['emoji']}</div>", 
                       unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <h2 style='margin-top: 0; color: {classification_style['color']};'>
                    {classification_style['label']}
                </h2>
                <div style='display: flex; align-items: center; gap: 1rem;'>
                    <div style='flex-grow: 1; background: rgba(0,0,0,0.1); height: 8px; border-radius: 4px;'>
                        <div style='width: {confidence*100:.0f}%; height: 100%; background: {classification_style['color']}; border-radius: 4px;'></div>
                    </div>
                    <span>{confidence:.0%} confidence</span>
                </div>
            """, unsafe_allow_html=True)

    # Main content columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🔍 Key Findings")
            if 'keywords' in result and result['keywords']:
                st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.5rem 0;'>", 
                           unsafe_allow_html=True)
                for keyword in result['keywords'][:10]:
                    st.markdown(f"""
                        <span style='
                            background: {classification_style['color']};
                            color: white;
                            padding: 0.3rem 0.6rem;
                            border-radius: 1rem;
                            font-size: 0.9rem;
                            font-weight: 600;
                        '>{keyword}</span>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No specific keywords identified")

    with col2:
        with st.container(border=True):
            st.markdown("### 🧠 Detailed Analysis")
            if 'reasoning' in result:
                st.markdown(f"""
                    <div style='
                        padding: 1rem;
                        background: rgba(0,0,0,0.03);
                        border-radius: 8px;
                        margin: 0.5rem 0;
                    '>
                        {result['reasoning']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No detailed reasoning provided")

    # Recommended Action
    action = result.get('action', 'N/A').capitalize()
    action_style = {
        "review": {"color": "#ff9800", "emoji": "👀"},
        "approve": {"color": "#2e7d32", "emoji": "✅"},
        "allow": {"color": "#2e7d32", "emoji": "✅"},
        "block": {"color": "#d32f2f", "emoji": "❌"},
        "remove": {"color": "#d32f2f", "emoji": "❌"}
    }.get(action.lower(), {"color": "#2196f3", "emoji": "❓"})

    with st.container(border=True):
        st.markdown("### 🚦 Recommended Action")
        st.markdown(f"""
            <div style='
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1rem;
                background: rgba(0,0,0,0.03);
                border-radius: 8px;
                margin: 0.5rem 0;
                border-left: 4px solid {action_style['color']};
            '>
                <span style='font-size: 2rem;'>{action_style['emoji']}</span>
                <h2 style='margin: 0; color: {action_style['color']};'>{action}</h2>
            </div>
        """, unsafe_allow_html=True)

    st.caption(f"⏱️ Analysis completed at: {result.get('timestamp', 'N/A')}")