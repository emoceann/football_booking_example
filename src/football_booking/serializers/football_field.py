from typing import Mapping, Sequence

from pydantic import TypeAdapter

from src.core.serializers.base import BaseSerializer, BaseListSerializer
from src.football_booking.schemas.fields import FootballFieldDetail, FootballFieldBase

football_field_adapter = TypeAdapter(list[FootballFieldBase])


class FootballFieldSerializer(BaseSerializer, BaseListSerializer):
    def serialize(self, data: Mapping) -> FootballFieldDetail:
        return FootballFieldDetail.model_validate(data)

    def serialize_list(self, data: Sequence[Mapping]) -> list[FootballFieldBase]:
        return football_field_adapter.validate_python(data, from_attributes=True)
