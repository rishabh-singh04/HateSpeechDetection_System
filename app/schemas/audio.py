# app/schemas/audio.py

from pydantic import BaseModel
from typing import Optional, Union
from enum import Enum

class InputType(str, Enum):
    base64 = "base64"
    file = "file"
    recording = "recording"

class AudioRequest(BaseModel):
    input_type: InputType
    audio_data: Optional[str] = None  # Base64 encoded audio
    language: str = "en"
    
    class Config:
        schema_extra = {
            "example": {
                "input_type": "base64",
                "audio_data": "BASE64_STRING",
                "language": "en"
            }
        }

class AudioResponse(BaseModel):
    text: str
    language: str
    processing_time_ms: int
    confidence: Optional[int] = None
    error: Optional[str] = None