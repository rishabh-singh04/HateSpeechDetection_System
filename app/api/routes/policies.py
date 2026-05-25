# app/api/routes/policies.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.policy import PolicyDocument
from app.services.policy_service import PolicyService
from app.schemas.policies import PolicyDocumentResponse, PolicySearchResponse
from datetime import datetime
import time
from typing import List
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

@router.get("/", response_model=List[PolicyDocumentResponse])
async def list_policies(db: Session = Depends(get_db)):
    """List all policy documents"""
    try:
        policies = db.query(PolicyDocument).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "content": p.content,
                "score": None,  # No score for full list
                "source": None
            }
            for p in policies
        ]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

