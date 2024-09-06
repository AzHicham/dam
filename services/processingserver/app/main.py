"""
Imageserver.
"""
import io
import uuid
from pathlib import Path
from typing import Annotated

from PIL import Image, ImageFilter
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from app import __version__
from app.config import settings
from app.logging import setup_logger
from app.schemas import BlurProcessingRequest, Status, ServiceStatus, Format
from app.client import ImageServerClient

logger = setup_logger()

app = FastAPI(debug=settings.DEBUG)

imageserver_client = ImageServerClient(server_url=settings.IMAGESERVER.URL)


def _get_image(id: uuid.UUID) -> Path:
    path = Path(settings.CACHE.DIR) / str(id)
    if path.exists():
        return path
    else:
        # We need a client to download the image from the Imageserver
        image = imageserver_client.download(id)
        with open(path, "wb") as f:
            f.write(image)
        return path


@app.get("/v0/processing/blur/{id}")
async def gaussian_blur(
    id: uuid.UUID,
    query: Annotated[BlurProcessingRequest, Depends(BlurProcessingRequest)]
):
    logger.info(f"Checking for image {id} in cache")
    try:
        path = _get_image(id)
        logger.info(f"Applying Gaussian blur with sigma={query.sigma} to {path}")
        image = Image.open(path).filter(ImageFilter.GaussianBlur(radius=query.sigma))
        logger.info(f"Applied Gaussian blur with sigma={query.sigma} to {path}")
    except (OSError, ValueError) as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    logger.info(query.format)
    buf = io.BytesIO()
    image.save(buf, query.format.value, quality=query.quality)
    buf.seek(0)

    return StreamingResponse(buf, media_type=f"image/{query.format.value}")


@app.get("/v0/status", response_model=ServiceStatus, tags=["Healthcheck"])
async def status():
    # Add checks on cache, ie is it RW ?
    # Add info about the cache ?
    return ServiceStatus(status=Status.Ready, version=__version__)
