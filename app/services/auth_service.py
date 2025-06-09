# app/services/auth_service.py

from fastapi import Response 
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.user import get_user_by_username
from app.schemas.user import UserResponse
from app.crud.user import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# In auth_service.py
def authenticate_user(db: Session, identifier: str, password: str):
    print(f"Attempting login with identifier: {identifier}")
    # Try username first
    user = get_user_by_username(db, identifier)
    
    # If not found by username, try email
    if not user:
        print("Not found by username, trying email")
        user = get_user_by_email(db, identifier)
    
    if not user:
        print("User not found")
        return None
        
    print(f"Found user: {user.username}")
    print(f"Password match: {verify_password(password, user.hashed_password)}")
    
    if not verify_password(password, user.hashed_password):
        return None
        
    return user

# def create_access_token(data: dict, user: UserResponse):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, 
#         settings.SECRET_KEY, 
#         algorithm=settings.ALGORITHM
#     )
#     return {
#         "access_token": encoded_jwt,
#         "token_type": "bearer",
#         "user": user
#     }

def create_access_token(response: Response, data: dict, user: UserResponse):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    # Set secure HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {encoded_jwt}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/" # send cookies to all paths and endpoints
    )
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "user": user
    }