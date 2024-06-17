from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from core import settings
from database.database import SessionLocal
from utils.minio import MinioClient


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_minio_client() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.s3.ACCESS_KEY,
        secret_key=settings.s3.SECRET_KEY,
        bucket_name=settings.s3.BUCKET_NAME,
        endpoint=settings.s3.s3_dns,
    )
    return minio_client
