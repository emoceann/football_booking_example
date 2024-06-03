from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.routes import router as auth_router
from src.core.exception_handlers.no_permission import no_permission
from src.core.exception_handlers.no_result_found import not_found
from src.core.exceptions.no_permission import NoPermission
from src.core.exceptions.not_found import NotFound
from src.core.settings import get_settings
from src.football_booking.routes import football_router, booking_router
from src.server.lifespan import lifespan

settings = get_settings()


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(football_router, prefix="/football", tags=["field football"])
    app.include_router(booking_router, prefix="/booking", tags=["booking"])
    app.exception_handler(NoPermission)(no_permission)
    app.exception_handler(NotFound)(not_found)
    app.mount("/static", StaticFiles(directory=settings.MEDIA_DIR, check_dir=False), name="static")
    return app
