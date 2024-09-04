from fastapi_users.db import TortoiseUserDatabase

from app.auth.models import UserDB, UserModel


async def get_user_db():
    yield TortoiseUserDatabase(UserDB, UserModel)