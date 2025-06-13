# frontend/app.py

import os
import sys
from pathlib import Path
import streamlit as st
from datetime import datetime
import base64

# Get the absolute path to the frontend directory
frontend_dir = str(Path(__file__).parent)
# Get the absolute path to the project root directory (two levels up)
project_root = str(Path(__file__).parent.parent.parent)

# Add both to Python path
sys.path.insert(0, frontend_dir)
sys.path.insert(0, project_root)

# Now import your modules
from components.audio_recorder import add_audio_listener, audio_recorder_component
from components.common import api_request, setup_page_config, load_assets
from pages.login_register import show_auth_page
from components.auth import show_sidebar

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
setup_page_config()

def main():
    load_assets()
    add_audio_listener()
    
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
                try:
                    # Ensure audio_data is bytes before passing to st.audio
                    if isinstance(st.session_state.audio_data, str):
                        audio_bytes = base64.b64decode(st.session_state.audio_data)
                    else:
                        audio_bytes = st.session_state.audio_data
                    st.audio(audio_bytes, format="audio/wav")
                except Exception as e:
                    st.error(f"Error playing audio: {str(e)}")
            with col2:
                if st.button("🗑️ Clear Recording", key="clear_recording_button"):
                    st.session_state.audio_data = None
                    st.rerun()
            with col3:
                if st.button("💾 Save Recording", key="save_recording_button"):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.session_state.transcriptions.append({
                        'timestamp': timestamp,
                        'audio': st.session_state.audio_data,
                        'transcription': None
                    })
                    st.success("Recording saved!")

        # Display history
        if st.session_state.get('transcriptions'):
            st.markdown("---")
            st.subheader("📜 Transcription History")
            
            for idx, item in enumerate(st.session_state.transcriptions):
                with st.expander(f"Recording {idx+1} - {item['timestamp']}"):
                    col1, col2 = st.columns([3,1])
                    with col1:
                        try:
                            audio_bytes = base64.b64decode(item['audio']) if isinstance(item['audio'], str) else item['audio']
                            st.audio(audio_bytes, format="audio/wav")
                            if item['transcription']:
                                st.json(item['transcription'])
                        except Exception as e:
                            st.error(f"Error displaying recording: {str(e)}")
                    with col2:
                        if st.button(f"Delete #{idx+1}", key=f"tab1_delete_button_{idx}"):
                            del st.session_state.transcriptions[idx]
                            st.rerun()
    
    with tab2:
        st.header("📜 Transcription History")
        if not st.session_state.transcriptions:
            st.info("No saved recordings yet")
        else:
            for idx, item in enumerate(st.session_state.transcriptions):
                with st.expander(f"Recording {idx+1} - {item['timestamp']}"):
                    col1, col2 = st.columns([3,1])
                    with col1:
                        try:
                            audio_bytes = base64.b64decode(item['audio']) if isinstance(item['audio'], str) else item['audio']
                            st.audio(audio_bytes, format="audio/wav")
                            if item['transcription']:
                                st.json(item['transcription'])
                        except Exception as e:
                            st.error(f"Error displaying recording: {str(e)}")
                    with col2:
                        if st.button(f"Transcribe #{idx+1}", key=f"transcribe_button_{idx}"):
                            with st.spinner("Transcribing..."):
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
                                    st.toast("Transcription complete!", icon="🎙️")
                                    st.rerun()
                        if st.button(f"Delete #{idx+1}", key=f"tab2_delete_button_{idx}"):
                            if st.confirm("Are you sure you want to delete this recording?"):
                                del st.session_state.transcriptions[idx]
                                st.rerun()
    
    with tab3:
        st.header("📊 Content Dashboard")
        st.write("Content analysis tools will appear here")
    
    # Notification handling
    if st.session_state.get('notification'):
        st.toast(st.session_state.notification, icon="✅")
        del st.session_state.notification

if __name__ == "__main__":
    main()