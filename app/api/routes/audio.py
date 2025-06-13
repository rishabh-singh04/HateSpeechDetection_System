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
    if not request.audio_data:
        return AudioResponse(
            text="",
            language=request.language,
            processing_time_ms=0,
            error="No audio data provided"
        )
    
    result = processor.transcribe(request.audio_data, request.language)
    return AudioResponse(
        text=result["text"],
        language=result["language"],
        processing_time_ms=result["processing_time_ms"],
        confidence=result.get("confidence"),
        error=result.get("error")
    )


@router.post("/transcribe-file", response_model=AudioResponse)
async def transcribe_file(file: UploadFile, language: str = "en"):
    """Endpoint for file uploads"""
    audio_data = base64.b64encode(await file.read()).decode("utf-8")
    result = processor.transcribe(audio_data, language)
    return AudioResponse(
        text=result["text"],
        language=result["language"],
        processing_time_ms=result["processing_time_ms"],
        confidence=result.get("confidence")
    )
