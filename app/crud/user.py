# app/crud/user.py

from sqlalchemy.orm import Session
from app.db.models.user import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def get_current_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    return user




