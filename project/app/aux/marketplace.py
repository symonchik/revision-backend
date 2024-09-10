from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List

from fastapi import HTTPException, status
from app.models.product import Product, Product_Pydantic, ProductIn_Pydantic, Purchase
from app.models.marketpl import Marketplace, Marketplace_Pydantic

import requests


async def update_ozon_products_list(
        marketplaces_id: List[str],
        user_id: int
):
    """
    get list of MP id
    get auth params
    get products id
    """

    for mp in marketplaces_id:
        # products = [p.mp_product_id for p in await Product.get(marketplace_id=mp).all()]

        # Marketplace_Pydantic.from_queryset_single(Marketplace.get(id=current_user.id))
        # Product_Pydantic.from_queryset_single(Product.get(marketplace_id=mp))
        # return []
        # User_Pydantic.from_queryset(User.all())
        prod_in_mp = await Product.filter(marketplace_id=mp).all().values('mp_product_id')

        products = [p.model_dump()['mp_product_id'] for p in prod_in_mp]

        host = 'https://api-seller.ozon.ru/v2/product/list'
        marketplace = await Marketplace_Pydantic.from_queryset_single(Marketplace.get(id=mp))
        
        headers = {
            'Client-id': marketplace.auth_data['client_id'],
            'Api-Key': marketplace.auth_data['api_key'],
        }

        response = requests.post(host, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        uuid = response.json()

        for product in uuid['result']['items']:
            if str(product['product_id']) not in products:
                prod_info = 'https://api-seller.ozon.ru/v2/product/info'
                data = {
                    "product_id": product['product_id']
                }
                response = requests.post(prod_info, json=data, headers=headers)
                if response.status_code != 200:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                prod__info = response.json()['result']

                product_obj = await Product.create(
                    mp_product_id=product['product_id'],
                    name=prod__info['name'],
                    marketplace_id=mp,
                    user_id=user_id,
                    price=int(float(prod__info['price'])),
                    sku=prod__info['sku'],
                    stocks_present=prod__info['stocks']['present']
                )
                await product_obj.save()

        
async def update_product_purchases(
        user_id: int,
        product_id: int,
        marketplaces_id: int
        
):
    """
    Function to update products purchses
    """
    marketplace = await Marketplace_Pydantic.from_queryset_single(Marketplace.get(id=marketplaces_id))
        
    headers = {
            'Client-id': marketplace.auth_data['client_id'],
            'Api-Key': marketplace.auth_data['api_key'],
        }
    
    date_now = datetime.now()

    data_json = {
        "dir": "ASC",
        "filter": {
            "order_id": 0,
            "since": (date_now - relativedelta(month=5)).isoformat() + "Z",
            "status": "delivered",
            "to": date_now.isoformat() + "Z",

            },
            "limit": 100,
            "offset": 0,

    }
    host = 'https://api-seller.ozon.ru/v3/posting/fbs/list'
    response = requests.post(host, json=data_json, headers=headers)
    uuid = response.json()
    for post in uuid['result']["postings"]:
        for prod in post["products"]:
            purchse_obj = await Purchase.create(
                            amount = prod["quantity"],
                            address = post["addressee"],
                            date = post["in_process_at"],
                            price = int(float(prod["price"])),
                            sku = prod["sku"],
                            prodict = product_id
                        )

