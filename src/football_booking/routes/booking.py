from fastapi import APIRouter, Depends, status

from src.auth.dependencies.get_current_user import get_user
from src.core.depedencies.check_permissions import check_if_manager, check_if_user
from src.football_booking.controller import FootballFieldInteractController
from src.football_booking.schemas.booking import Booking, BookingOut

router = APIRouter()


@router.get(
    "/delete/{booking_id}",
    dependencies=[Depends(get_user), Depends(check_if_manager)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_football_field(
        booking_id: int,
        controller: FootballFieldInteractController = Depends()
):
    return await controller.delete_book(booking_id)


@router.post(
    "/create",
    dependencies=[Depends(get_user), Depends(check_if_user)],
    status_code=status.HTTP_201_CREATED
)
async def create_booking(
        data: Booking,
        controller: FootballFieldInteractController = Depends()
):
    return await controller.book_field(data)


@router.get(
    "/field/{field_name}",
    dependencies=[Depends(get_user), Depends(check_if_manager)],
    response_model=list[BookingOut]
)
async def get_bookings_for_field(
        field_name: str,
        controller: FootballFieldInteractController = Depends()
):
    return await controller.get_bookings_for_field(field_name)
