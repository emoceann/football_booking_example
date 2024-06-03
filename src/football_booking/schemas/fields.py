from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import BaseModel


class FootballFieldBase(BaseModel):
    name: str
    booking_rate: int


class FootballFieldDetail(FootballFieldBase):
    contact: str
    lon: float
    lat: float
    images: list[str]


class FootballFieldCreate(FootballFieldDetail):
    images: list[UploadFile]

    @classmethod
    def as_form(
            cls,
            images: list[UploadFile],
            name: str = Form(),
            booking_rate: int = Form(),
            contact: str = Form(),
            lon: float = Form(),
            lat: float = Form()
    ):
        return cls.model_construct(
            images=images,
            name=name,
            booking_rate=booking_rate,
            contact=contact,
            lat=lat,
            lon=lon
        )


class FootballFieldUpdate(BaseModel):
    booking_rate: int | None = None
    contact: str | None = None
    lon: float | None = None
    lat: float | None = None
    images: list[UploadFile] | None = None

    @classmethod
    def as_form(
            cls,
            images: Annotated[list[UploadFile], None] = None,
            booking_rate: int | None = Form(None),
            contact: str | None = Form(None),
            lon: float | None = Form(None),
            lat: float | None = Form(None)
    ):
        return cls.model_construct(
            images=images,
            booking_rate=booking_rate,
            contact=contact,
            lat=lat,
            lon=lon
        )
