# # app/api/routes/audio.py

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from tempfile import NamedTemporaryFile
# from app.schemas.moderation import ModerationResponse
# from app.services.audio_moderation_service import moderate_audio_content
# from app.core.exceptions import AudioProcessingError

# router = APIRouter()

# @router.post("/moderate", 
#            response_model=ModerationResponse,
#            summary="Moderate audio content")
# async def moderate_audio(
#     file: UploadFile = File(..., description="Audio file to moderate")
# ):
#     try:
#         with NamedTemporaryFile(delete=True) as temp_audio:
#             temp_audio.write(file.file.read())
#             temp_audio.seek(0)
#             return moderate_audio_content(temp_audio.name)
#     except AudioProcessingError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Audio processing failed")