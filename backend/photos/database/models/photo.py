import uuid
from uuid import UUID

from pydantic import BaseConfig
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from .base import ModelBase

if TYPE_CHECKING:
    from .user import UserModel


class PhotoBase(SQLModel):
    image_url: str = Field(index=True, schema_extra={'"json_schema_extra"': "http://192.0.2.10:9001/memes/kubernetes_static_website.png"})
    description: str = Field(index=True, schema_extra={'"json_schema_extra"': "Kubernetes static website"})


class PhotoModel(PhotoBase, ModelBase, table=True):
    __tablename__ = "photos"
    user_id: UUID = Field(foreign_key="users.id", index=True, default=uuid.uuid4())

    user: 'UserModel' = Relationship(back_populates="photos")

    class Config(BaseConfig):
        arbitrary_types_allowed = True