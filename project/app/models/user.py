from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt

# class UserLogin(Model):
#     """
#     model for login and registration.
#     Only 2 fields required 
#     """
#     email = fields.CharField(max_length=50, unique=True) # add validators for this field
#     password_hash =  fields.CharField(max_length=128, null=False)

# UserLogin_Pydantic = pydantic_model_creator(UserLogin, name='User', exclude_readonly=True)

class User(Model):
    # user_id = fields.IntField(primary_key=True)
    account_type = fields.CharField(max_length=50, default="base user")
    name = fields.CharField(max_length=50, default="air distributor")
    email = fields.CharField(max_length=50, unique=True) # add validators for this field
    password_hash = fields.CharField(max_length=128, null=False) # fastapi users
    phone_number = fields.CharField(max_length=13, unique=True, null=True)
    account_status = fields.CharField(max_length=50, default="unsubscribed") # need create class of status
    is_active = fields.BooleanField(default=False)
    # created_at = fields.DatetimeField(auto_now_add=True)
    # paymnet_expired_at = fields.DatetimeField()
    # marketplaces = fields.ForeignKeyField('models.ForeginMarketplace', related_name='mps')

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

class UserToken(Model):
    """
    не надо
    """
    token = fields.UUIDField(max_length=36, pk=True)
    user = fields.ForeignKeyField('models.User', related_name='user')
    created_at = fields.DatetimeField(null=True, auto_now_add=True, use_tz=False)


UserToken_Pydantic = pydantic_model_creator(UserToken, name='UserToken')
UserTokenIn_Pydantic = pydantic_model_creator(UserToken, name='UserTokenIn', exclude_readonly=True)
