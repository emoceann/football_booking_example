from functools import cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int

    JWT_ENCRYPT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_SECONDS: int

    MEDIA_DIR: str


@cache
def get_settings() -> Settings:
    return Settings()
