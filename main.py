from fastapi import FastAPI

from app.api.auth.routers import auth_router
from app.api.users.routers import users_router
from app.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    application = FastAPI(version="1.0.0")

    application.add_event_handler(
        "startup",
        create_start_app_handler(),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(),
    )
    application.include_router(users_router)
    application.include_router(auth_router)

    return application


app = get_application()
