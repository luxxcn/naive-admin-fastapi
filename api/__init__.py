from fastapi import FastAPI

from config.secure import DEBUG
from . import auth, user, role, permission


def register_routers(app: FastAPI):
    prefix = "/api"  # if DEBUG else "/prod-api"

    app.include_router(auth.api, prefix=prefix)
    app.include_router(user.api, prefix=prefix)
    app.include_router(role.api, prefix=prefix)
    app.include_router(permission.api, prefix=prefix)
