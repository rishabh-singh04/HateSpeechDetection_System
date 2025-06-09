# app/api/routes/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.api.dependencies import get_current_user


router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    try:
        return create_user(user_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete accounts"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}