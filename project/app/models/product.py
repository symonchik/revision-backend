from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
# from pydantic import BaseModel


class Product(Model):
    user = fields.ForeignKeyField('models.User', related_name='product_user', on_delete=fields.CASCADE)
    marketplace = fields.ForeignKeyField('models.Marketplace', related_name='product_marketplace', on_delete=fields.CASCADE)

    mp_product_id = fields.TextField()
    market = fields.CharField(max_length=50, default="ozon")
    name = fields.CharField(max_length=50, default="good")
    sku = fields.IntField(default=1)
    price = fields.IntField(default=100)
    discount = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now=True)
    sale_schema = fields.CharField(max_length=50, default="fbo")
    category = fields.CharField(max_length=50, default="product")
    stocks_present = fields.IntField(default=1)
    

Product_Pydantic = pydantic_model_creator(Product, name='Product')
ProductIn_Pydantic = pydantic_model_creator(Product, name='ProductIn', exclude_readonly=True)

class Purchase(Model):
    product = fields.ForeignKeyField('models.Product', related_name='purchase_product', on_delete=fields.CASCADE)
    amount = fields.IntField(default=1)
    address = fields.CharField(max_length=100, default="good")
    date = fields.DatetimeField(auto_now=True)
    price = fields.IntField(default=100)
    sku = fields.IntField(default=1)
    
    # marketplace =  fields.ForeignKeyField('models.User', related_name='product_user', on_delete=fields.CASCADE)

Purchase_Pydantic = pydantic_model_creator(Purchase, name='Purchase')
PurchaseIn_Pydantic = pydantic_model_creator(Product, name='PurchaseIn', exclude_readonly=True)

