# frontend/components/audio_recorder.py
import streamlit as st
import base64
from components.common import api_request
import time
from datetime import datetime


def audio_recorder_component():
    """Improved audio recorder with better state management"""
    # Initialize session state for recording status
    if 'recording_status' not in st.session_state:
        st.session_state.recording_status = "Ready to record"
    
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
    .recording {
        background-color: #ffcccc;
        color: #cc0000;
    }
    .ready {
        background-color: #ccffcc;
        color: #006600;
    }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript for recording
    recorder_js = """
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let stream;

    async function startRecording() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.start(100); // Collect data every 100ms
            document.getElementById('status').className = 'recording-status recording';
            document.getElementById('status').textContent = "Recording...";
            
            // Automatically stop after 2 minutes
            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    stopRecording();
                }
            }, 120000);
            
        } catch (error) {
            console.error("Recording error:", error);
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
                    resolve(base64data);
                    audioChunks = [];
                    
                    // Stop all tracks
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
    </script>
    """

    # Inject the JavaScript
    st.components.v1.html(recorder_js)
    
    # Recording controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Start Recording"):
            st.session_state.recording_status = "Recording..."
            st.components.v1.html("""
            <script>
            window.startRecording();
            </script>
            """)
    
    with col2:
        if st.button("⏹ Stop Recording"):
            st.session_state.recording_status = "Processing..."
            st.components.v1.html("""
            <script>
            window.stopRecording().then(base64data => {
                window.parent.postMessage({
                    type: 'audioData',
                    data: base64data
                }, '*');
            });
            </script>
            """, height=0)
    
    # Status display
    status_class = "recording" if "Recording" in st.session_state.recording_status else "ready"
    st.markdown(
        f'<div id="status" class="recording-status {status_class}">{st.session_state.recording_status}</div>',
        unsafe_allow_html=True
    )

    # Handle audio data from JavaScript
    if st.session_state.get('audio_data'):
        st.audio(st.session_state.audio_data, format="audio/wav")
        
        transcribe_col, save_col = st.columns(2)
        with transcribe_col:
            if st.button("📡 Transcribe Audio", key="transcribe_main"):
                with st.spinner("Transcribing audio..."):
                    start_time = time.time()
                    try:
                        response = api_request(
                            "POST",
                            "/transcribe",
                            json={
                                "audio_data": st.session_state.audio_data,
                                "language": "en"
                            },
                            timeout=30  # Increased timeout for longer audio
                        )
                        
                        if response and response.status_code == 200:
                            transcription = response.json()
                            processing_time = time.time() - start_time
                            
                            # Add processing time to results
                            transcription['processing_time'] = f"{processing_time:.2f}s"
                            st.session_state.transcription = transcription
                            
                            # Save to history
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.transcriptions.append({
                                'timestamp': timestamp,
                                'audio': st.session_state.audio_data,
                                'transcription': transcription
                            })
                            
                            st.success("Transcription complete!")
                            st.json(transcription)
                        else:
                            st.error(f"Transcription failed: {response.text if response else 'No response'}")
                    except Exception as e:
                        st.error(f"Transcription error: {str(e)}")

    # JavaScript message listener
    st.components.v1.html("""
    <script>
    window.addEventListener('message', (event) => {
        if (event.data.type === 'audioData') {
            window.parent.streamlitSessionState.set(
                {'audio_data': event.data.data},
                {from_js: true}
            );
        }
    });
    </script>
    """, height=0)