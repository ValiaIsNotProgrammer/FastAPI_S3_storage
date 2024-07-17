import uuid

from pydantic import BaseModel, EmailStr

from core.security import pwd_context
from database.models.user import UserBase
from database.models.base import ModelBase


class UserRead(UserBase, ModelBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": str(uuid.uuid4()),
                "email": "YourMail@example.com",
                "hashed_password": pwd_context.hash("EXAMPLE_PASSWORD"),
                # "photos": list[PhotoModel.model_config]
            }
        }
    }


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "YourMail@example.com",
                "password": "StrongPassword",
            }
        }
    }


class UserUpdate(UserCreate):
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "YourMail@example.com",
                "password": "StrongPassword",
            }
        }
    }


