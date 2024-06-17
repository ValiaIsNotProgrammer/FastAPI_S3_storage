from fastapi import APIRouter

from api.api_v1.endpoints.photos import router as photos_router


api_router = APIRouter()

api_router.include_router(photos_router, prefix="/photos", tags=["photos"])