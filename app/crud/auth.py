# app/crud/auth.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from fastapi import Response
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.user import User
from app.schemas.user import UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(
    db: Session,
    password: str,
    username: Optional[str] = None,
    email: Optional[str] = None
) -> Optional[User]:
    user = None
    if username:
        user = db.query(User).filter(User.username == username).first()
    elif email:
        user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.is_active:
        return None
        
    if not pwd_context.verify(password, user.hashed_password):
        return None
        
    return user

def create_access_token(
    response: Response,
    username: str,
    user: UserResponse,
    expires_delta: Optional[timedelta] = None
):
    try:
        expire = datetime.utcnow() + (expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ))
        
        encoded_jwt = jwt.encode(
            {"sub": username, "exp": expire},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
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

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None