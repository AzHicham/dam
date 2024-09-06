import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Format(Enum):
    JPEG = "jpeg"
    PNG = "png"


class ImageRequest(BaseModel):
    format: Format = Field(
        default=Format.JPEG,
        alias="f",
        description="Format of the image",
        examples=["jpeg"],
    )
    quality: int = Field(
        default=80,
        alias="q",
        description="Quality of the image, valid for JPEG only",
        examples=[80],
    )


class Status(Enum):
    Ready = "Ready"
    NotReady = "NotReady"


class ServiceStatus(StrictModel):
    status: Status = Field(
        ...,
        description="Status of the service",
        examples=["Ready"],
    )
    version: str = Field(
        ...,
        description="Version of the service",
        examples=["0.1.0"],
    )


class ImageUploadResponse(StrictModel):
    id: uuid.UUID = Field(
        description="Id of the uploaded image",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
