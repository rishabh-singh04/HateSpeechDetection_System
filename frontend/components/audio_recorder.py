# frontend/components/audio_recorder.py
import streamlit as st
from components.common import api_request
import base64
from datetime import datetime

def audio_recorder_component():
    """Audio recorder using HTML5 and Streamlit components"""
    st.markdown("""
    <style>
    .audio-container {
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    if 'audio_bytes' not in st.session_state:
        st.session_state.audio_bytes = None
    if 'transcription' not in st.session_state:
        st.session_state.transcription = None

    # Tab interface
    tab1, tab2 = st.tabs(["🎤 Record Audio", "📁 Upload Audio"])

    with tab1:
        st.markdown("<div class='audio-container'>", unsafe_allow_html=True)
        st.markdown("### Live Recording")
        
        # Custom audio recorder using HTML/JS
        recorder_html = """
        <script>
        let mediaRecorder;
        let audioChunks = [];
        
        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.ondataavailable = event => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                mediaRecorder.start();
                document.getElementById('status').textContent = "Recording...";
                document.getElementById('stopBtn').disabled = false;
                document.getElementById('startBtn').disabled = true;
                
            } catch (error) {
                console.error("Error accessing microphone:", error);
                document.getElementById('status').textContent = "Error: " + error.message;
            }
        }
        
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const reader = new FileReader();
                    
                    reader.onload = function() {
                        const base64data = reader.result.split(',')[1];
                        window.parent.postMessage({
                            type: 'audioData',
                            data: base64data
                        }, '*');
                    };
                    
                    reader.readAsDataURL(audioBlob);
                    audioChunks = [];
                    document.getElementById('status').textContent = "Recording stopped";
                    document.getElementById('stopBtn').disabled = true;
                    document.getElementById('startBtn').disabled = false;
                };
            }
        }
        </script>
        
        <div>
            <button id="startBtn" onclick="startRecording()">Start Recording</button>
            <button id="stopBtn" disabled onclick="stopRecording()">Stop Recording</button>
            <p id="status">Ready to record</p>
        </div>
        """
        
        st.components.v1.html(recorder_html, height=150)
        
        # Handle audio data from JS
        if st.session_state.get('audio_data'):
            try:
                # Decode the base64 audio data
                audio_bytes = base64.b64decode(st.session_state.audio_data)
                st.session_state.audio_bytes = audio_bytes
                st.audio(audio_bytes, format="audio/wav")
            except Exception as e:
                st.error(f"Error playing audio: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='audio-container'>", unsafe_allow_html=True)
        st.markdown("### File Upload")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3", "ogg", "m4a"],
            accept_multiple_files=False,
            key="audio_file_uploader"
        )
        
        if uploaded_file:
            audio_bytes = uploaded_file.read()
            st.session_state.audio_bytes = audio_bytes
            st.session_state.audio_data = base64.b64encode(audio_bytes).decode("utf-8")
            st.success("File uploaded!")
            st.audio(audio_bytes, format=uploaded_file.type)
        st.markdown("</div>", unsafe_allow_html=True)

    # Transcription button for both methods
    if st.session_state.get('audio_data'):
        if st.button("✨ Transcribe Audio", key="transcribe_button"):
            with st.spinner("Processing..."):
                try:
                    response = api_request(
                        "POST",
                        "/audio/transcribe",
                        json={
                            "input_type": "base64",
                            "audio_data": st.session_state.audio_data,
                            "language": "en"
                        },
                        timeout=30
                    )
                    
                    if response and response.status_code == 200:
                        st.session_state.transcription = response.json()
                        st.success("Transcription successful!")
                        st.json(st.session_state.transcription)
                        
                        # Save to history
                        if 'transcriptions' not in st.session_state:
                            st.session_state.transcriptions = []
                        
                        st.session_state.transcriptions.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'audio': st.session_state.audio_data,
                            'transcription': st.session_state.transcription
                        })
                    else:
                        st.error("Transcription failed")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    
        add_audio_listener()

        if st.button("🗑️ Clear Audio", key="clear_audio_button"):
            st.session_state.audio_data = None
            st.session_state.audio_bytes = None
            st.session_state.transcription = None
            st.rerun()

def add_audio_listener():
    st.components.v1.html("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'audioData') {
            window.parent.streamlitSessionState.set({
                'audio_data': event.data.data
            }, true);
        }
    });
    </script>
    """, height=0)