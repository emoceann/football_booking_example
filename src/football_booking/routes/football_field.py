from fastapi import APIRouter, Depends, status

from src.auth.dependencies.get_current_user import get_user
from src.core.depedencies.check_permissions import check_if_user, check_if_manager
from src.football_booking.controller import FootballFieldInteractController
from src.football_booking.schemas.fields import FootballFieldBase, FootballFieldDetail, FootballFieldCreate, \
    FootballFieldUpdate
from src.football_booking.schemas.filters import FilterFields

router = APIRouter()


@router.get(
    "/filter",
    dependencies=[Depends(get_user), Depends(check_if_user)],
    response_model=list[FootballFieldBase]
)
async def get_football_fields(
        filters: FilterFields = Depends(),
        controller: FootballFieldInteractController = Depends()
):
    return await controller.get_football_fields(filters)


@router.get(
    "/detail/{field_name}",
    dependencies=[Depends(get_user), Depends(check_if_user)],
    response_model=FootballFieldDetail
)
async def get_football_field_detail(
        field_name: str,
        controller: FootballFieldInteractController = Depends()
):
    return await controller.get_detailed_football_info(field_name)


@router.post(
    "/add",
    dependencies=[Depends(get_user), Depends(check_if_manager)],
    status_code=status.HTTP_201_CREATED
)
async def create_football_field(
        data: FootballFieldCreate = Depends(FootballFieldCreate.as_form),
        controller: FootballFieldInteractController = Depends()
):
    return await controller.add_football_field(data)


@router.patch(
    "/update/{field_name}",
    dependencies=[Depends(get_user), Depends(check_if_manager)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_football_field(
        field_name: str,
        data: FootballFieldUpdate = Depends(FootballFieldUpdate.as_form),
        controller: FootballFieldInteractController = Depends()
):
    return await controller.update_football_field(data, field_name)
