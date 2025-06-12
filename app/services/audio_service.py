# app/services/audio_service.py
import whisper
import tempfile
import base64
import os
from typing import Tuple
from fastapi import HTTPException, status

class AudioProcessor:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load Whisper model (small by default)"""
        if self.model is None:
            self.model = whisper.load_model("small")
        return self.model
    
    def process_audio(self, audio_data: str, language: str = "en") -> Tuple[str, str, int]:
        """
        Process base64 encoded audio data and return transcription, language, and confidence
        
        Args:
            audio_data: Base64 encoded audio data
            language: Expected language code (e.g., "en")
            
        Returns:
            Tuple of (transcription, detected_language, confidence_score)
        """
        try:
            model = self.load_model()
            
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                tmpfile.write(audio_bytes)
                tmpfile_path = tmpfile.name
            
            # Transcribe audio
            result = model.transcribe(tmpfile_path, language=language)
            
            # Clean up
            os.unlink(tmpfile_path)
            
            return (
                result.get("text", ""),
                result.get("language", language),
                int(result.get("confidence", 0.8) * 100)  # Convert to percentage
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Audio processing failed: {str(e)}"
            )