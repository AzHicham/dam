from pathlib import Path

import aiofiles
from fastapi import UploadFile


async def save_upload_file(file: UploadFile, destination: Path) -> None:
    destination.parent.mkdir(exist_ok=True, parents=True)
    async with aiofiles.open(destination, "wb") as out_file:
        while content := await file.read(1024 * 1024):  # async read chunk
            if isinstance(content, bytes):
                await out_file.write(content)  # async write chunk
