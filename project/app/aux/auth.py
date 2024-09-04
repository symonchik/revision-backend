from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
import fastapi_users
# from fastapi_users.authentication import (
#     AuthenticationBackend,
#     BearerTransport,
#     JWTStrategy,
# )
# from fastapi_users.manager import UserManager

# from app.models.tortoise import User
from app.auth.models import UserDB
from app.auth.users import current_active_user, auth_backend

# from dotenv import load_dotenv
# import os
# load_dotenv()
# SECRET_AUTH = os.environ.get("SECRET_AUTH")


check_router = APIRouter()

SECRET_AUTH = "not_so_secret"

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router()
reset_password_router = fastapi_users.get_reset_password_router()
verify_router = fastapi_users.get_verify_router()
users_router = fastapi_users.get_users_router()

check_router = APIRouter()

@check_router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}