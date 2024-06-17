from sqlmodel import SQLModel, Field, UUID

from .base import ModelBase


class PhotoBase(SQLModel):
    image_url: str = Field(index=True, schema_extra={'"json_schema_extra"': "http://192.0.2.10:9001/memes/kubernetes_static_website.png"})
    description: str = Field(index=True, schema_extra={'"json_schema_extra"': "Kubernetes static website"})


class PhotoModel(PhotoBase, ModelBase, table=True):
    __tablename__ = "photos"