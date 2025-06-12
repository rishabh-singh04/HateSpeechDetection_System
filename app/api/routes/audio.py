# app/api/routes/audio.py
from fastapi import APIRouter, UploadFile
from app.services.whisper_service import WhisperRealtime
from app.schemas.audio import AudioRequest, AudioResponse
import base64

router = APIRouter(prefix="", tags=["audio"])
processor = WhisperRealtime(model_size="base")  # Initialize once

@router.post("/transcribe", response_model=AudioResponse)
async def transcribe_base64(request: AudioRequest):
    """Endpoint for base64 audio data"""
    return processor.transcribe(request.audio_data, request.language)

@router.post("/transcribe-file", response_model=AudioResponse)
async def transcribe_file(file: UploadFile, language: str = "en"):
    """Endpoint for file uploads"""
    audio_data = base64.b64encode(await file.read()).decode("utf-8")
    return processor.transcribe(audio_data, language)
