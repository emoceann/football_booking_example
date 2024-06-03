from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.controller import AuthController
from src.auth.schemas.token import TokenData
from src.auth.schemas.user import UserIn

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def test_example(
        data: UserIn,
        controller: AuthController = Depends()
):
    return await controller.create_user(data)


@router.post(
    "/token",
    response_model=TokenData
)
async def get_auth_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        controller: AuthController = Depends()
):
    return await controller.check_credentials(form_data)
