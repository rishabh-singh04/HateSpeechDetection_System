# app/api/routes/moderation.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.db.session import get_db
from app.services.moderation_service import moderate_content
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.moderation import ExportRequest, ModerationResult
from app.data.exports.moderation_exports import ModerationExporter
import logging
from datetime import datetime
router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@router.post("/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return moderate_content(request.text, db)
    except Exception as e:
        logger.error(f"Moderation failed: {str(e)}")
        return ModerationResponse(
            action="block",
            classification="error",
            reasoning=f"Moderation failed: {str(e)}",
            timestamp=datetime.utcnow().isoformat(),
            confidence=0.0,
            keywords=[]
        )