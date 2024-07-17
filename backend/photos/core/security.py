from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from core import settings
from schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(str.encode(settings.security.ENCRYPT_KEY))


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def __create_access_token(data: TokenData, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # data.update({"exp": expire})
    data.expire = expire
    encoded_jwt = jwt.encode(data.model_dump(mode='json'), settings.security.SECRET_KEY, algorithm=settings.security.HASH_ALGORITHM)
    return encoded_jwt


def get_data_encrypt(data) -> str:
    data = fernet.encrypt(data)
    return data.decode()


def create_access_token(sub: UUID) -> str:
    access_token_expires = timedelta(minutes=settings.security.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = TokenData(sub=sub)
    access_token = __create_access_token(
        token_data, expires_delta=access_token_expires
    )
    return access_token


def get_content(variable: str) -> str:
    return fernet.decrypt(variable.encode()).decode()