from datetime import datetime

from pydantic import BaseModel, FutureDatetime, field_validator, ValidationInfo


class Booking(BaseModel):
    name: str
    start_date: FutureDatetime
    finish_date: FutureDatetime

    @field_validator("finish_date", mode="after")
    def check_if_later(cls, value, context: ValidationInfo) -> FutureDatetime:
        if not context.data.get("start_date") < value:
            raise ValueError("start date should not be bigger than finish_date")
        return value


class BookingOut(Booking):
    id: int
    start_date: datetime
    finish_date: datetime
