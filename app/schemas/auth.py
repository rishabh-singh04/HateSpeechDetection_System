# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        model_config = ConfigDict(from_attributes=True)