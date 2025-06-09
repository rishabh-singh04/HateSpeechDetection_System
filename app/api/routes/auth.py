# app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.schemas.user import UserResponse
from app.db.session import get_db
from app.services.auth_service import authenticate_user, create_access_token
from app.services.user_service import create_user
from app.schemas.user import UserCreate
from app.db.models.user import User
from app.crud.user import get_user_by_email
from app.api.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate and return token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert SQLAlchemy user to Pydantic model
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat() if user.updated_at else None
    )
    
    # Create access token and set it in the response cookie
    return create_access_token(
        response=response,
        data={"sub": user.username},
        user=user_response
    )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        return create_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user)
):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at.isoformat(),
        updated_at=current_user.updated_at.isoformat() if current_user.updated_at else None
    )