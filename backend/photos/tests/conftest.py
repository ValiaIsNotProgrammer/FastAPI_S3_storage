import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

engine = create_async_engine(
    url=settings.db.pg_dns
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)