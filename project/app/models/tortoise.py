from tortoise import fields, models
from fastapi_users import models as users_models

from tortoise.contrib.pydantic import pydantic_model_creator


class TextSummary(models.Model):
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)

# class ForeginMarketplace(models.Model):
#     """
#     Class. all marketplaces that can
#     be accessed will be in a separate database.

#     marketplace_id - pk
#     auth_data - data for auth, differs for different marketplaces
#     """
#     marketplace_id = fields.IntField(primary_key=True)
#     # seller_id = fields.ForeignKeyField('models.Seller', related_name='sellers') # rly need it?
#     mp_name = fields.TextField()
#     auth_data = fields.JSONField()

# class User(users_models.BaseUser, models.BaseUser):
#     user_id = fields.IntField(primary_key=True)
#     account_type = fields.TextField()
#     name = fields.TextField(max_length=50, unique=True)
#     email = fields.TextField(unique=True)
#     password_hash = fields.TextField() # fastapi users
#     phone_number = fields.TextField()
#     account_status = fields.TextField() # need create class of status
#     created_at = fields.DatetimeField(auto_now_add=True)
#     paymnet_expired_at = fields.DatetimeField()
#     # marketplaces = fields.ForeignKeyField('models.ForeginMarketplace', related_name='mps')


# class UserCreate(users_models.BaseUserCreate):
#     pass

# class UserUpdate(users_models.BaseUserUpdate):
#     pass

# class UserModel(TortoiseBaseUserModel):
#     pass

# class Product(models.Model):
#     product_id = fields.IntField(primary_key=True)
#     mp_id = fields.ForeignKeyField()
#     seller_id = fields.ForeignKeyField()
#     name = fields.TextField()
#     stock_quantity = fields.IntField()
#     category = fields.TextField() # need create class of status
#     tags = fields.TextField() # need create class of status
#     sell_shema = fields.TextField() # need create class of status
#     created_at = fields.DatetimeField(auto_now_add=True)
#     price = fields.IntField()
#     price_discount = fields.IntField()


# class Order(models.Model):
#     order_id = fields.IntField(primary_key=True)
#     product_id = fields.ForeignKeyField()
#     seller_id = fields.ForeignKeyField()
#     order_date = fields.DatetimeField(auto_now_add=True)
#     delivery_status = fields.TextField() # need create class of status
#     total_amount = fields.IntField()
#     delivery_address = fields.TextField()
#     payment_status = fields.TextField()
#     payment_method = fields.TextField()
#     price = fields.IntField()