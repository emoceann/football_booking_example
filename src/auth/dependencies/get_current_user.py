from fastapi import Depends, Request

from src.auth.controller import oauth2_scheme, AuthController


async def get_user(
        request: Request,
        token: str = Depends(oauth2_scheme),
        controller: AuthController = Depends()
) -> None:
    request.state.user = await controller.get_current_user(token)
