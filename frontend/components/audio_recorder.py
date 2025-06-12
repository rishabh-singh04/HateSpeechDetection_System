# frontend/components/audio_recorder.py
import streamlit as st
import base64
from components.common import api_request
import time
from datetime import datetime

def audio_recorder_component():
    """Fixed audio recorder with proper JS-Streanlit communication"""
    # Initialize session states
    if 'recording_status' not in st.session_state:
        st.session_state.recording_status = "Ready to record"
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    if 'transcription' not in st.session_state:
        st.session_state.transcription = None

    # Main recorder UI
    st.markdown("""
    <style>
    .recording-status {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .recording { background-color: #ffcccc; color: #cc0000; }
    .ready { background-color: #ccffcc; color: #006600; }
    .error { background-color: #ffdddd; color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript for recording with improved message handling
    recorder_js = """
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let stream;

    function sendAudioToPython(base64data) {
        const data = {
            audio_data: base64data,
            is_audio: true
        };
        window.parent.postMessage(data, "*");
    }

    async function startRecording() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.start(100);
            document.getElementById('status').className = 'recording-status recording';
            document.getElementById('status').textContent = "Recording...";
            
            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    stopRecording();
                }
            }, 120000);
            
        } catch (error) {
            console.error("Recording error:", error);
            document.getElementById('status').className = 'recording-status error';
            document.getElementById('status').textContent = "Error: " + error.message;
        }
    }

    function stopRecording() {
        return new Promise(resolve => {
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                
                reader.onloadend = () => {
                    const base64data = reader.result.split(',')[1];
                    sendAudioToPython(base64data);
                    audioChunks = [];
                    
                    if (stream) {
                        stream.getTracks().forEach(track => track.stop());
                    }
                };
                
                reader.readAsDataURL(audioBlob);
            };
            
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
            
            document.getElementById('status').className = 'recording-status ready';
            document.getElementById('status').textContent = "Recording stopped";
        });
    }

    window.startRecording = startRecording;
    window.stopRecording = stopRecording;

    // Listen for Streamlit ready event
    window.addEventListener('message', (event) => {
        if (event.data === 'streamlit:componentReady') {
            console.log('Streamlit component ready');
        }
    });
    </script>
    """

    # Inject the JavaScript
    st.components.v1.html(recorder_js, height=0)

    # Recording controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Start Recording"):
            st.components.v1.html("""
            <script>
            if (window.stopRecording) {
                window.stopRecording();
            }
            </script>
            """, height=0)
            st.session_state.recording_status = "Recording..."
    
    with col2:
        if st.button("⏹ Stop Recording"):
            
            st.components.v1.html("""
            <script>
            if (window.stopRecording) {
                window.stopRecording();
            }
            </script>
            """, height=0)
            st.session_state.recording_status = "Processing..."

    # Status display
    status_class = "recording" if "Recording" in st.session_state.recording_status else "ready"
    st.markdown(
        f'<div id="status" class="recording-status {status_class}">{st.session_state.recording_status}</div>',
        unsafe_allow_html=True
    )

    # # JavaScript message listener for audio data
    # st.components.v1.html("""
    # <script>
    # window.addEventListener('message', (event) => {
    #     if (event.data.is_audio) {
    #         const audioData = event.data.audio_data;
    #         window.parent.streamlitSessionState.set(
    #             {'audio_data': audioData},
    #             {from_js: true}
    #         );
    #     }
    # });
    # </script>
    # """, height=0)

    # Handle the audio data
    if st.session_state.get('audio_data'):
        st.audio(st.session_state.audio_data, format="audio/wav")
        
        if st.button("📡 Transcribe Audio"):
            with st.spinner("Transcribing..."):
                try:
                    response = api_request(
                        "POST",
                        "/transcribe",
                        json={
                            "audio_data": st.session_state.audio_data,
                            "language": "en"
                        },
                        timeout=30
                    )
                    
                    if response and response.status_code == 200:
                        st.session_state.transcription = response.json()
                        st.success("Transcription successful!")
                        st.json(st.session_state.transcription)
                    else:
                        st.error("Transcription failed")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Force a rerun to update the UI after receiving audio
    if st.session_state.get('audio_data_updated', False):
        st.session_state.audio_data_updated = False
        st.rerun()