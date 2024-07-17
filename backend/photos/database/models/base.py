from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class ModelBase(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Optional[UUID] = Field(primary_key=True, index=True, default=uuid4(), schema_extra={"json_schema_extra": str(uuid4())})