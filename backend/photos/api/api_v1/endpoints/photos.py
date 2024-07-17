from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_minio_client, get_session, get_current_user
from database.models.photo import PhotoModel
from database.models.user import UserModel
from database.repo.photos import repo
from schemas.photo import PhotoRead
from utils.minio import MinioClient

router = APIRouter()


@router.get("/", response_model=List[PhotoRead], status_code=status.HTTP_200_OK)
async def get_photos(offset: int = 0,
                     limit: int = 10,
                     session: AsyncSession = Depends(get_session),
                     current_user: UserModel = Depends(get_current_user)):
    photos = await repo.get_multi_paginated_by_user(session=session, limit=limit, offset=offset, user=current_user)
    return photos


@router.get("/{id}", response_model=PhotoRead, status_code=status.HTTP_200_OK)
async def get_photo(id: UUID,
                    session: AsyncSession = Depends(get_session),
                    current_user: UserModel = Depends(get_current_user)):
    photo = await repo.get_photo_by_user(photo_id=id, user=current_user, session=session)
    return photo


@router.post("/", response_model=PhotoRead, status_code=status.HTTP_201_CREATED)
async def create_photo(description: str = Form(...),
                       file: UploadFile = File(...),
                       session: AsyncSession = Depends(get_session),
                       minio_client: MinioClient = Depends(get_minio_client),
                       current_user: UserModel = Depends(get_current_user)):
    image_url = minio_client.upload_image(file)
    photo = PhotoModel(description=description, image_url=image_url, user=current_user)
    new_photo = await repo.create(photo, session=session)
    return new_photo.dict()


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(id: UUID, session: AsyncSession = Depends(get_session),
                       current_user: UserModel = Depends(get_current_user),
                       minio_client: MinioClient = Depends(get_minio_client)):
    photo = await repo.get_photo_by_user(photo_id=id, user=current_user, session=session)
    image_url = photo.image_url
    minio_client.delete_image(image_url)
    return await repo.delete_photo_by_user(photo_id=id, session=session, user=current_user)


@router.put("/", response_model=PhotoRead, status_code=status.HTTP_200_OK)
async def update_photo(id: Optional[UUID] = Form(...),
                       description: Optional[str] = Form(None),
                       file: UploadFile = File(None),
                       session: AsyncSession = Depends(get_session),
                       minio_client: MinioClient = Depends(get_minio_client),
                       current_user: UserModel = Depends(get_current_user)):

    if not any((file, description)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one of 'file' or 'description' must be provided"
        )

    photo: PhotoModel = await repo.get_photo_by_user(photo_id=id, session=session, user=current_user)
    image_url = photo.image_url

    if file:
        updated_image_url = minio_client.update_image(image_url, file)
        photo.image_url = updated_image_url
    if description:
        photo.description = description
    db_photo = await repo.update_photo_by_user(photo=photo, session=session, user=current_user)
    return db_photo

