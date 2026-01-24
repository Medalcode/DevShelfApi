from fastapi import APIRouter
from .routes import resources, auth

api_router = APIRouter()
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
