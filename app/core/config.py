# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    SQLALCHEMY_DATABASE_URL: str
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ENDPOINT: Optional[str] = None
    OPENAI_VERSION: Optional[str] = "2023-12-01-preview"
    OPENAI_MODEL: Optional[str] = "gpt-4o"

    # Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ENVIRONMENT: str = "development"  # or "production"

    class Config:
        env_file = ".env"
        extra = "ignore"  # This will ignore extra env variables

settings = Settings()