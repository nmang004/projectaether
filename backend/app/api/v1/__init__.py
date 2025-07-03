"""API v1 router module."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, sites

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])