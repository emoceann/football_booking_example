import aiofiles
from aiofiles import os as asyncos
from fastapi import UploadFile


async def create_folder(path: str) -> None:
    if await asyncos.path.exists(path):
        return
    await asyncos.mkdir(path=path)


async def save_file_to_folder(file_path: str, media: UploadFile) -> None:
    async with aiofiles.open(file_path, "wb") as file:
        await file.write(await media.read())
        await file.flush()
