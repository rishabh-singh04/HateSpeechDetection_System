# app/services/user_service.py

from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse
from passlib.context import CryptContext
from datetime import datetime

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_user(user_data: UserCreate, db: Session) -> UserResponse:
    """
    Create a new user in the database
    
    Args:
        user_data: UserCreate schema with registration data
        db: Database session
    
    Returns:
        UserResponse with created user data
    
    Raises:
        ValueError: If username or email already exists
    """
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise ValueError("Username already registered")
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("Email already registered")
    
    # Create user model
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        is_superuser=False,
        created_at=datetime.utcnow()
    )
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Return response model
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        is_superuser=db_user.is_superuser,
        created_at=db_user.created_at.isoformat(),
        updated_at=db_user.updated_at.isoformat() if db_user.updated_at else None
    )