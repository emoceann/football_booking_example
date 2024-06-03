from fastapi import Depends, Request
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID
from sqlalchemy import table, column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.config import get_session
from src.core.exceptions.no_permission import NoPermission
from src.football_booking.repositories.base import AbstractManagmentRepo
from src.football_booking.schemas.booking import BookingOut
from src.football_booking.schemas.fields import FootballFieldUpdate
from src.football_booking.serializers.bookings import BookingSerializer


class ManagmentRepoInteract(AbstractManagmentRepo):
    def __init__(
            self,
            request: Request,
            session: AsyncSession = Depends(get_session),
            serializer: BookingSerializer = Depends()
    ):
        self.session = session
        self.user = request.state.user
        self.request = request
        self.serializer = serializer
        self.football_table = table(
            "football_fields",
            column("name"),
            column("contact"),
            column("geom", Geometry(geometry_type='POINT', srid=4326)),
            column("images", JSONB),
            column("booking_rate"),
            column("owner_id")
        )

    async def get_bookings_for_field(self, field_name: str) -> list[BookingOut]:
        stmt = text(
            "select bookings.id, start_date, finish_date, field_name as name from bookings "
            "left join football_fields on bookings.field_name = football_fields.name "
            "where football_fields.name = :field_name and owner_id = :owner_id"
        ).bindparams(field_name=field_name, owner_id=self.user.id)
        res = await self.session.execute(stmt)
        mapped_res = res.mappings().all()
        return self.serializer.serialize_list(mapped_res)

    async def delete_booking_for_field(self, booking_id: int) -> None:
        stmt = text(
            "select football_fields.id from football_fields "
            "left join bookings on football_fields.name = bookings.field_name "
            "where owner_id = :owner_id and bookings.id = :booking_id"
        ).bindparams(owner_id=self.user.id, booking_id=booking_id)
        res = await self.session.execute(stmt)
        if not res:
            raise NoPermission(message="You can't delete")
        stmt = text("delete from bookings where id = :booking_id").bindparams(
            booking_id=booking_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def add_football_field(self, football_field_data: dict) -> None:
        stmt = self.football_table.insert().values(
            owner_id=self.user.id,
            geom=ST_SetSRID(ST_MakePoint(football_field_data.pop("lat"), football_field_data.pop("lon")), 4326),
            **football_field_data
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_football_field(self, field_update_data: FootballFieldUpdate, field_name: str) -> None:
        stmt = self.football_table.update().where(
            text("name = :field_name").bindparams(field_name=field_name)
        )
        if field_update_data.lat and field_update_data.lon:
            stmt = stmt.values(geom=ST_SetSRID(
                ST_MakePoint(field_update_data.lat, field_update_data.lon), 4326
            ))
        stmt = stmt.values(**field_update_data.model_dump(exclude_none=True, exclude={"lat", "lon"}))
        await self.session.execute(stmt)
        await self.session.commit()
