# app/api/routes/policies.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.policy import PolicyDocument
from app.services.policy_service import search_policies
from app.schemas.policies import PolicyDocumentResponse, PolicySearchResponse
from datetime import datetime
import time
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PolicyDocumentResponse])
async def list_policies(db: Session = Depends(get_db)):
    """List all policy documents"""
    try:
        policies = db.query(PolicyDocument).all()
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=PolicySearchResponse)
async def search_policies_endpoint(
    query: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Search policy documents"""
    try:
        start_time = time.time()
        results = await search_policies(query, limit, db)
        search_time = (time.time() - start_time) * 1000
        
        # Convert SQLAlchemy models to Pydantic models
        policy_responses = [
            PolicyDocumentResponse(
                id=policy.id,
                name=policy.name,
                content=policy.content,
                score=getattr(policy, 'score', None)
            ) for policy in results
        ]
        
        return PolicySearchResponse(
            results=policy_responses,
            search_time_ms=search_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

