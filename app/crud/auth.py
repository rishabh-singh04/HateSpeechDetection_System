# app/crud/auth.py

from jose import jwt, JWTError

from datetime import datetime, timedelta
from app.core.config import settings

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