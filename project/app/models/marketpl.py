from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel



class OZONApiKeys(BaseModel):
    client_id: str
    api_key: str


class Marketplace(Model):
    """
    Class. all marketplaces that can
    be accessed will be in a separate database.

    marketplace_id - pk
    auth_data - data for auth, differs for different marketplaces
    """
    mp_name = fields.TextField()
    auth_data = fields.JSONField() # use hash
    user = fields.ForeignKeyField('models.User', related_name='marketplace_user', on_delete=fields.CASCADE)

Marketplace_Pydantic = pydantic_model_creator(Marketplace, name='MarketPlace')
MarketplaceIn_Pydantic = pydantic_model_creator(Marketplace, name='MarketPlaceIn', exclude_readonly=True)