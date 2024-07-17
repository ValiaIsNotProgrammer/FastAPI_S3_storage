from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


class PGConfig(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DATABASE: str

    @property
    def pg_dns(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class PhotosRunConfig(BaseModel):
    HOST: str
    PORT: int


class APIConfig(BaseModel):
    CURRENT_VERSION: str


class S3Config(BaseModel):
    HOST: str
    PORT: int
    ACCESS_KEY: str
    SECRET_KEY: str
    USER: str
    PASSWORD: str
    BUCKET_NAME: str

    @property
    def s3_dns(self):
        return f"{self.HOST}:{self.PORT}"


class SecurityConfig(BaseModel):
    SECRET_KEY: str
    ENCRYPT_KEY: str
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_CONFIG__",
                                      env_nested_delimiter="__", case_sensitive=False)

    db: PGConfig
    run: PhotosRunConfig
    api: APIConfig
    s3: S3Config
    security: SecurityConfig


settings = Settings()