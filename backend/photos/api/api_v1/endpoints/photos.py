from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_session, get_minio_client
from database.repo.photos import repo
from schemas.photo import PhotoCreate, PhotoRead, PhotoUpdate
from utils.minio import MinioClient

router = APIRouter()


@router.get("/memes", response_model=List[PhotoRead], status_code=status.HTTP_200_OK)
async def get_photos(offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    photos = await repo.get_multi_paginated(session=session, limit=limit, offset=offset)
    return photos


@router.get("/memes/{id}", response_model=PhotoRead, status_code=status.HTTP_200_OK)
async def get_photo(id: str, session: AsyncSession = Depends(get_session)):
    photo = await repo.get_by_id(id, session=session)
    return photo


@router.post("/memes", response_model=PhotoRead, status_code=status.HTTP_201_CREATED)
async def create_photo(description: str = Form(...),
                       file: UploadFile = File(...),
                       session: AsyncSession = Depends(get_session),
                       minio_client: MinioClient = Depends(get_minio_client)):
    image_url = minio_client.upload_image(file)
    photo = PhotoCreate(description=description, image_url=image_url)
    new_photo = await repo.create(photo, session=session)
    return new_photo.dict()


@router.put("/memes/{id}", response_model=PhotoRead, status_code=status.HTTP_200_OK)
async def update_photo(id: str, photo: PhotoUpdate, session: AsyncSession = Depends(get_session)):
    db_photo = await repo.update(id, photo, session=session)
    return db_photo


@router.delete("/memes/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(id: str, session: AsyncSession = Depends(get_session)):
    return await repo.delete(id, session=session)
