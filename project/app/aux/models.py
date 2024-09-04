from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise import fields, models
from fastapi_users import models as users_models


class User(users_models.BaseUser, models.BaseUser):
    user_id = fields.IntField(primary_key=True)
    account_type = fields.TextField()
    name = fields.TextField(max_length=50, unique=True)
    email = fields.TextField(unique=True)
    password_hash = fields.TextField() # fastapi users
    phone_number = fields.TextField()
    account_status = fields.TextField() # need create class of status
    created_at = fields.DatetimeField(auto_now_add=True)
    paymnet_expired_at = fields.DatetimeField()
    # marketplaces = fields.ForeignKeyField('models.ForeginMarketplace', related_name='mps')


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserModel(TortoiseBaseUserModel):
    pass


class UserDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel
