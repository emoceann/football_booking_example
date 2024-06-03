from fastapi import Depends, Request
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.config import get_session
from src.core.exceptions.no_permission import NoPermission
from src.core.exceptions.not_found import NotFound
from src.football_booking.repositories.base import AbstractUserInteractRepo
from src.football_booking.schemas.fields import FootballFieldBase, FootballFieldDetail
from src.football_booking.schemas.filters import FilterFields
from src.football_booking.serializers.football_field import FootballFieldSerializer


class UserRepoInteract(AbstractUserInteractRepo):
    def __init__(
            self,
            request: Request,
            session: AsyncSession = Depends(get_session),
            serializer: FootballFieldSerializer = Depends()
    ):
        self.session = session
        self.user = request.state.user
        self.request = request
        self.serializer = serializer

    async def create_book_field(self, data: dict) -> None:
        stmt = text(
            "select id from bookings where (bookings.start_date, bookings.finish_date) overlaps (:start_date, :finish_date) and field_name = :name"
        ).bindparams(
            **data
        )
        res = await self.session.scalar(
            stmt
        )
        if res:
            raise NoPermission(message="Interval is occupied")
        stmt = text("select id from football_fields where name = :name").bindparams(name=data.get("name"))
        res = await self.session.scalar(
            stmt
        )
        if not res:
            raise NotFound(message="football field not found")
        stmt = text(
            "insert into bookings(field_name, start_date, finish_date, user_book) "
            "values (:name, :start_date, :finish_date, :user_book)"
        ).bindparams(
            **data,
            user_book=self.user.id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_football_fields(self, filters: FilterFields) -> list[FootballFieldBase]:
        stmt = select(text("name, booking_rate")).select_from(text("football_fields"))
        if filters.date_gte and filters.date_lte:
            stmt = stmt.join(
                target=text("bookings"),
                onclause=text(
                    "football_fields.name = bookings.field_name and bookings.start_date > :date_start and bookings.finish_date < :date_finish"
                ).bindparams(date_start=filters.date_gte, date_finish=filters.date_lte),
                isouter=True
            )
        else:
            stmt = stmt.join(
                target=text("bookings"),
                onclause=text("football_fields.name = bookings.field_name"),
                isouter=True
            )
        stmt = stmt.where(
            text("bookings is null")
        ).order_by(text("geom <-> st_setsrid(st_point(:lon_x, :lat_y), 4326)").bindparams(
            lon_x=filters.lon_x, lat_y=filters.lat_y
        ))
        res = await self.session.execute(stmt)
        mapped_res = res.mappings().all()
        return self.serializer.serialize_list(mapped_res)

    async def get_detail_football_fields(self, field_name: str) -> FootballFieldDetail:
        stmt = text(
            "select name, contact, st_x(st_transform(geom, 4326)) as lon, st_y(st_transform(geom, 4326)) as lat, images, booking_rate "
            "from football_fields where name = :field_name"
        ).bindparams(field_name=field_name)
        res = await self.session.execute(stmt)
        mapped_res = res.mappings().first()
        if not mapped_res:
            raise NotFound(message="football field not found")
        return self.serializer.serialize(mapped_res)
