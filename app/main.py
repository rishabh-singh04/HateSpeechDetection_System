# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import moderation, policies, user, auth

app = FastAPI(
    title="Content Moderation API",
    description="API for content moderation with policy enforcement",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(moderation.router, prefix="/moderation", tags=["moderation"])
app.include_router(policies.router, prefix="/policies", tags=["policies"])