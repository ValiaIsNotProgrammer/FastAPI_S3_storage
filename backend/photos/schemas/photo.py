from fastapi import Form, File, UploadFile
from sqlmodel import SQLModel, Field

from database.models.photo import PhotoBase
from database.models.base import ModelBase


class PhotoRead(PhotoBase, ModelBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class PhotoCreate(SQLModel):
    description: str = Field(schema_extra={"example": "Bruh description"})
    image_url: str = Field(schema_extra={"example": "localhost:9001/memes/foo.png"})


class PhotoDelete(ModelBase):
    status: int = 204

