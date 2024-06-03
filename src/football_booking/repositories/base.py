from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from src.football_booking.schemas.booking import Booking, BookingOut
from src.football_booking.schemas.fields import FootballFieldBase, FootballFieldDetail


class AbstractManagmentRepo(ABC):
    @abstractmethod
    async def add_football_field(self, football_field_data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_football_field(self, field_update_data: FootballFieldDetail, field_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_bookings_for_field(self, filters: Any) -> list[BookingOut]:
        raise NotImplementedError

    @abstractmethod
    async def delete_booking_for_field(self, booking_id: int) -> None:
        raise NotImplementedError


class AbstractUserInteractRepo(ABC):
    @abstractmethod
    async def create_book_field(self, data: Booking) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_football_fields(self, data: BaseModel) -> list[FootballFieldBase]:
        raise NotImplementedError

    @abstractmethod
    async def get_detail_football_fields(self, field_name: str) -> FootballFieldDetail:
        raise NotImplementedError
