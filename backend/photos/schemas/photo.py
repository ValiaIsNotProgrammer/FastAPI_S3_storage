from sqlmodel import SQLModel, Field

from database.models.photo import PhotoBase, PhotoModel


class PhotoRead(PhotoModel):
    pass


class PhotoUpdate(PhotoBase):
    pass


class PhotoCreate(SQLModel):
    description: str = Field(schema_extra={"example": "Bruh description"})
    image_url: str = Field(schema_extra={"example": "localhost:9001/memes/foo.png"})


class PhotoDelete(PhotoBase):
    pass
