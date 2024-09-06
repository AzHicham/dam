import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Format(Enum):
    JPEG = "jpeg"
    PNG = "png"


class BlurProcessingRequest(BaseModel):
    sigma: float = Field(
        description="Sigma value for the Gaussian blur",
        alias="s",
        examples=[1.5],
    )
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
