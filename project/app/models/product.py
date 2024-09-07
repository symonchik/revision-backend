from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
# from pydantic import BaseModel


class Product(Model):
    mp_product_id = fields.TextField()
    name = fields.CharField(max_length=50, default="good")
    price = fields.IntField(default=100)
    created_at = fields.DatetimeField(auto_now=True)
    sale_schema = fields.CharField(max_length=50, default="fbo")
    category = fields.CharField(max_length=50, default="product")


    user = fields.ForeignKeyField('models.User', related_name='product_user', on_delete=fields.CASCADE)
    marketplace = fields.ForeignKeyField('models.Marketplace', related_name='marketplaces', on_delete=fields.CASCADE)

Product_Pydantic = pydantic_model_creator(Product, name='Product')
ProductIn_Pydantic = pydantic_model_creator(Product, name='ProductIn', exclude_readonly=True)