from pydantic import BaseModel, FutureDatetime


class FilterBookings(BaseModel):
    date_gte: FutureDatetime | None = None
    date_lte: FutureDatetime | None = None
    field_name: str


class FilterFields(BaseModel):
    lon_x: float
    lat_y: float
    date_gte: FutureDatetime | None = None
    date_lte: FutureDatetime | None = None
