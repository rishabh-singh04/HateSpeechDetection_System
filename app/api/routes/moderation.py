# app/api/routes/moderation.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.schemas.classification_result import HateSpeechClassificationResult
from app.db.session import get_db
from app.services.moderation_service import moderate_content

router = APIRouter()

@router.post("/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    db: Session = Depends(get_db)
):
    """Moderate text content against policies"""
    try:
        return moderate_content(request.text, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    