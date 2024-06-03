from fastapi import Request

from src.core.exceptions.no_permission import NoPermission


async def check_if_manager(
        request: Request
) -> None:
    if request.state.user.type not in ["manager", "admin"]:
        raise NoPermission


async def check_if_user(
        request: Request
) -> None:
    if request.state.user.type not in ["user", "admin"]:
        raise NoPermission
