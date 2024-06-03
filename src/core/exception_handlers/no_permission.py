from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from src.core.exceptions.no_permission import NoPermission


async def no_permission(request: Request, exc: NoPermission):
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "code": status.HTTP_403_FORBIDDEN, "error": exc.message
        }
    )
