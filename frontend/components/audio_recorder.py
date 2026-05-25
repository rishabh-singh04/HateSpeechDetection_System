# frontend/components/audio_recorder.py
import streamlit as st
from components.common import api_request
import base64
import hashlib

def generate_unique_key(prefix: str) -> str:
    """Generate a unique Streamlit widget key based on session id."""
    session_id = st.session_state.get('session_id', 'default')
    return f"{prefix}_{hashlib.md5(session_id.encode()).hexdigest()[:8]}"

def audio_recorder_component():
    """
    Audio upload component:
    - Uploads audio file (wav, mp3, ogg, m4a)
    - Sends base64 audio data to API for transcription
    - Returns transcription JSON if successful, else None
    """
    unique_key = generate_unique_key("audio_uploader")
    
    st.markdown("""
    <style>
    .audio-container {
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        background: var(--card-bg);
        transition: all 0.3s ease;
    }
    .audio-container:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

    transcription_result = None

    with st.container():
        st.markdown("<div class='audio-container'>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload audio file (MP3, WAV, OGG, M4A)",
            type=["wav", "mp3", "ogg", "m4a"],
            key=unique_key,
            accept_multiple_files=False,
            help="Upload audio to transcribe its content"
        )

        if uploaded_file:
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format=uploaded_file.type)

            # Encode audio to base64
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

            with st.spinner("Transcribing audio..."):
                try:
                    response = api_request(
                        "POST",
                        "audio/transcribe",
                        json={
                            "input_type": "base64",
                            "audio_data": audio_b64,
                            "language": "en"
                        },
                        timeout=30
                    )
                    if response and response.status_code == 200:
                        transcription_result = response.json()
                        st.success("Transcription successful!")
                    else:
                        st.error("Failed to transcribe audio.")
                except Exception as e:
                    st.error(f"Transcription error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    return transcription_result
