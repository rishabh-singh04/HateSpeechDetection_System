# app/schemas/token.py

from pydantic import BaseModel
from app.schemas.user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse  # Include user details in response

class TokenData(BaseModel):
    username: str | None = None