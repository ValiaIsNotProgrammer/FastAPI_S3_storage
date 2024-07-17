from fastapi import APIRouter

from api.api_v1.endpoints.photos import router as photos_router
from api.api_v1.endpoints.auth import router as auth_router


api_router = APIRouter()

api_router.include_router(photos_router, prefix="/photos", tags=["photos"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])