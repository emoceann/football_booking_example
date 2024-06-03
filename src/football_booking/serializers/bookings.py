from typing import Mapping, Sequence

from pydantic import TypeAdapter

from src.core.serializers.base import BaseListSerializer
from src.football_booking.schemas.booking import BookingOut

bookings = TypeAdapter(list[BookingOut])


class BookingSerializer(BaseListSerializer):
    def serialize_list(self, data: Sequence[Mapping]) -> list[BookingOut]:
        return bookings.validate_python(data)
