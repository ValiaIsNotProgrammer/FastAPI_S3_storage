from sqlmodel import Field

from .base import ModelBase


class UserModel(ModelBase, table=True):
    __tablename__ = "users"
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
