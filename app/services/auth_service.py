# app/services/auth_service.py

from fastapi import Response, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.user import get_user_by_username, get_user_by_email
from app.schemas.user import UserResponse
from app.db.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(
    db: Session, 
    password: str, 
    username: Optional[str] = None, 
    email: Optional[str] = None
) -> Optional[User]:
    try:
        user = None
        if username:
            user = get_user_by_username(db, username=username)
        elif email:
            user = get_user_by_email(db, email=email)
        
        if not user or not user.is_active:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    response: Response, 
    data: dict, 
    user: UserResponse,
    expires_delta: Optional[timedelta] = None
):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ))
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        # Set cookie with secure defaults
        response.set_cookie(
            key="access_token",
            value=f"Bearer {encoded_jwt}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=settings.SECURE_COOKIES,
            samesite="lax",
            path="/"
        )
        
        return {
            "access_token": encoded_jwt,
            "token_type": "bearer",
            "user": user
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token creation error: {str(e)}"
        )