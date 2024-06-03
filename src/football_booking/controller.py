import uuid

from fastapi import Depends, UploadFile

from src.core.settings import get_settings, Settings
from src.core.utils import save_file_to_folder
from src.football_booking.repositories.managment_repo import ManagmentRepoInteract
from src.football_booking.repositories.user_repo import UserRepoInteract
from src.football_booking.schemas.booking import Booking, BookingOut
from src.football_booking.schemas.fields import FootballFieldBase, FootballFieldDetail, FootballFieldCreate, \
    FootballFieldUpdate
from src.football_booking.schemas.filters import FilterFields


class FootballFieldInteractController:
    def __init__(
            self,
            repo: UserRepoInteract = Depends(),
            management_repo: ManagmentRepoInteract = Depends(),
            settings: Settings = Depends(get_settings)
    ):
        self.repo = repo
        self.management = management_repo
        self.settings = settings

    async def get_football_fields(self, filters: FilterFields) -> list[FootballFieldBase]:
        return await self.repo.get_football_fields(filters)

    async def get_detailed_football_info(self, field_name: str) -> FootballFieldDetail:
        return await self.repo.get_detail_football_fields(field_name)

    async def book_field(self, data: Booking) -> None:
        return await self.repo.create_book_field(data.model_dump())

    async def delete_book(self, booking_id: int) -> None:
        return await self.management.delete_booking_for_field(booking_id)

    async def get_bookings_for_field(self, field_name: str) -> list[BookingOut]:
        return await self.management.get_bookings_for_field(field_name)

    async def add_football_field(self, data: FootballFieldCreate) -> None:
        data.images = await self._save_images_to_dir(data.images)
        return await self.management.add_football_field(data.model_dump())

    async def update_football_field(self, data: FootballFieldUpdate, field_name: str) -> None:
        if data.images:
            data.images = await self._save_images_to_dir(data.images)
        return await self.management.update_football_field(data, field_name)

    async def _save_images_to_dir(self, images: list[UploadFile]):
        media_paths = []
        for i in images:
            _, file_format = i.content_type.split("/")
            path_to = f"{self.settings.MEDIA_DIR}/{uuid.uuid4()}.{file_format}"
            await save_file_to_folder(path_to, i)
            media_paths.append(path_to)
        return media_paths
