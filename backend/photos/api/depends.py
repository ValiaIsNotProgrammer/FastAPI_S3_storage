from typing import AsyncGenerator
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from core import settings
from database.database import SessionLocal
from database.repo.users import repo
from utils.minio import MinioClient


oauth2_scheme = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def authorization(token: str, session: AsyncSession, credentials_exception):
    try:
        payload = jwt.decode(token, settings.security.SECRET_KEY, algorithms=[settings.security.HASH_ALGORITHM])
        sub: UUID = payload.get("sub")
        if not sub:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    user = await repo.get_by_id(id=sub, session=session)
    if not user:
        raise credentials_exception
    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    access_token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await authorization(access_token, session, credentials_exception)


def get_minio_client() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.s3.ACCESS_KEY,
        secret_key=settings.s3.SECRET_KEY,
        bucket_name=settings.s3.BUCKET_NAME,
        endpoint=settings.s3.s3_dns,
    )
    return minio_client
