# app/schemas/audio.py
from pydantic import BaseModel

class AudioRequest(BaseModel):
    audio_data: str          # Base64 encoded audio
    language: str = "en"     # Optional language hint

class AudioResponse(BaseModel):
    text: str                # Transcription result
    language: str            # Detected language
    processing_time_ms: int  # Time taken (ms)