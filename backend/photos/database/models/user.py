from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr, BaseModel, field_validator, BaseConfig

from .base import ModelBase

if TYPE_CHECKING:
    from .photo import PhotoModel


class BcryptHash(BaseModel):
    hashed_password: str

    @field_validator('hashed_password')
    def validate_bcrypt_hash(cls, v):
        if len(v) != 60:
            raise ValueError('Bcrypt hash must be exactly 60 characters long')
        # Bcrypt hash regex pattern: $2[ayb]\$[0-9]{2}\$[./A-Za-z0-9]{53}
        if not v.startswith('$2') or not v[3].isdigit() or not v[4] == '$' or not v[5:]:
            raise ValueError('Invalid Bcrypt hash format')
        return v


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, nullable=False, schema_extra={"example": "uniquemail@outlook.com"})
    hashed_password: str = Field(sa_column=Column(String, index=True, unique=True), schema_extra={"example": "localhost:9001/memes/foo.png"})


class UserModel(ModelBase, UserBase, table=True):
    __tablename__ = "users"

    photos: list['PhotoModel'] = Relationship(back_populates="user")

    class Config(BaseConfig):
        arbitrary_types_allowed = True

