"""
Imageserver.
"""
import io
import uuid
from pathlib import Path
from typing import Annotated

from PIL import Image
from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from app import __version__
from app.config import settings
from app.logging import setup_logger
from app.schemas import ImageRequest, Status, ServiceStatus, Format, ImageUploadResponse
from app.utils import save_upload_file
from app.minio import MinioClient

logger = setup_logger()

app = FastAPI(debug=settings.DEBUG)

minio = MinioClient(
    settings.MINIO.URL,
    settings.MINIO.BUCKET,
    settings.MINIO.ACCESS_KEY,
    settings.MINIO.SECRET_KEY
)


def _get_image(id: uuid.UUID) -> Path:
    path = Path(settings.CACHE.DIR) / str(id)
    if path.exists():
        return path
    else:
        minio.download(str(id), Path(settings.CACHE.DIR) / str(id))
        return path


@app.get("/v0/imgsrv/{id}")
async def image(
    id: uuid.UUID,
    query: Annotated[ImageRequest, Depends(ImageRequest)]
):
    logger.info(f"Checking for image {id} in cache")
    try:
        path = _get_image(id)
        image = Image.open(path)
    except (OSError, ValueError) as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    logger.info(query.format)
    buf = io.BytesIO()
    image.save(buf, query.format.value, quality=query.quality)
    buf.seek(0)

    return StreamingResponse(buf, media_type=f"image/{query.format.value}")


@app.post(
    "/v0/imgsrv",
    status_code=201,
    response_model=ImageUploadResponse,
)
async def upload_file(file: UploadFile):
    # Generate a UUID for the image
    id = uuid.uuid4()
    # Save the file in the cache
    path = Path(settings.CACHE.DIR) / str(id)
    await save_upload_file(file, path)
    # Upload the file to S3
    minio.upload(str(id), path)
    return ImageUploadResponse(id=id)


@app.get("/v0/status", response_model=ServiceStatus, tags=["Healthcheck"])
async def status():
    return ServiceStatus(status=Status.Ready, version=__version__)
