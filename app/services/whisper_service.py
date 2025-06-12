# app/services/whisper_service.py
import whisper
import base64
import tempfile
import time
from typing import Dict

class WhisperRealtime:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)  # Load once at startup
    
    def transcribe(self, audio_base64: str, language: str = "en") -> Dict:
        """Process audio and return dict with text, language, and timing"""
        start_time = time.time()
        
        # Decode and save to temp file
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            result = self.model.transcribe(tmp.name, language=language)
        
        return {
            "text": result["text"],
            "language": result.get("language", language),
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }