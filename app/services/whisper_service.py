# app/services/whisper_service.py
import os
import whisper
import base64
import tempfile
import time
from typing import Dict

class WhisperRealtime:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)
    
    def transcribe(self, audio_base64: str, language: str = "en") -> Dict:
        start_time = time.time()
        
        try:
            audio_bytes = base64.b64decode(audio_base64)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp.flush()
                tmp.close()  # Explicitly close to ensure file is written
                result = self.model.transcribe(
                    tmp.name, 
                    language=language,
                    fp16=False  # Better compatibility
                )
                os.unlink(tmp.name) # Clean up temporary file
            
            return {
                "text": result["text"],
                "language": result.get("language", language),
                "processing_time_ms": int((time.time() - start_time) * 1000),
                "confidence": int(result.get("confidence", 0.8) * 100)
            }
        except Exception as e:
            return {
                "text": "",
                "language": language,
                "processing_time_ms": 0,
                "confidence": 0,
                "error": str(e)
            }