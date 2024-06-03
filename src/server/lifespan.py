from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.settings import get_settings
from src.core.utils import create_folder

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await create_folder(settings.MEDIA_DIR)
    yield
