from sqlalchemy import AsyncAdaptedQueuePool, NullPool
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine, AsyncEngine, \
    create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.photos.core.settings import settings


engine = create_async_engine(
    url=str(settings.db.pg_dns),
    echo=False,
    poolclass=NullPool
    # if core.MODE == ModeEnum.testing
    # else AsyncAdaptedQueuePool,  # Asincio pytest works with NullPool
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
