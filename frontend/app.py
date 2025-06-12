# frontend/app.py
import sys
from pathlib import Path
import streamlit as st
from datetime import datetime
from components.common import api_request

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'notification' not in st.session_state:
    st.session_state.notification = None
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'transcriptions' not in st.session_state:
    st.session_state.transcriptions = []

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
    
    # Main title with enhanced styling
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #f5d7a1;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    <div class="main-title">
        <h1>🛡️ Content Moderation Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive divider
    st.markdown("---")
    
    # Authentication check
    if not st.session_state.get('access_token'):
        show_auth_page()
        st.stop()
    
    # Main application layout
    from components.audio_recorder import audio_recorder_component
    from components.auth import show_sidebar
    
    # Create sidebar
    show_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["Audio Recorder", "Transcription History", "Dashboard"])
    
    with tab1:
        st.header("🎙️ Audio Recording")
        audio_recorder_component()
        
        # Audio playback and management
        if st.session_state.get('audio_data'):
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.audio(st.session_state.audio_data, format="audio/wav")
            with col2:
                if st.button("🗑️ Clear Recording"):
                    st.session_state.audio_data = None
                    st.rerun()
            with col3:
                if st.button("💾 Save Recording"):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.session_state.transcriptions.append({
                        'timestamp': timestamp,
                        'audio': st.session_state.audio_data,
                        'transcription': None
                    })
                    st.success("Recording saved!")
    
    with tab2:
        st.header("📜 Transcription History")
        if not st.session_state.transcriptions:
            st.info("No saved recordings yet")
        else:
            for idx, item in enumerate(st.session_state.transcriptions):
                with st.expander(f"Recording {idx+1} - {item['timestamp']}"):
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.audio(item['audio'], format="audio/wav")
                        if item['transcription']:
                            st.json(item['transcription'])
                    with col2:
                        if st.button(f"Transcribe #{idx+1}"):
                            with st.spinner("Processing..."):
                                response = api_request(
                                    "POST",
                                    "/transcribe",
                                    json={
                                        "audio_data": item['audio'],
                                        "language": "en"
                                    }
                                )
                                if response and response.status_code == 200:
                                    st.session_state.transcriptions[idx]['transcription'] = response.json()
                                    st.rerun()
                        if st.button(f"Delete #{idx+1}"):
                            del st.session_state.transcriptions[idx]
                            st.rerun()
    
    with tab3:
        st.header("📊 Content Dashboard")
        st.write("Content analysis tools will appear here")
        # Add your dashboard components here
    
    # Notification handling
    if st.session_state.get('notification'):
        st.toast(st.session_state.notification, icon="✅")
        del st.session_state.notification

if __name__ == "__main__":
    main()