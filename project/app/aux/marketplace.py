from typing import List

from fastapi import HTTPException, status
from app.models.product import Product, Product_Pydantic, ProductIn_Pydantic
from app.models.marketpl import Marketplace, Marketplace_Pydantic

import requests


async def update_ozon_products_list(
        marketplaces_id: List[str],
        user_id: int
)-> List[ProductIn_Pydantic]:
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
        prod_in_mp = await Product_Pydantic.from_queryset(Product.filter(marketplace_id=mp).all())
        print(prod_in_mp)
        products = [p.model_dump()['mp_product_id'] for p in prod_in_mp]
        # products = []
        # print(products)

        host = 'https://api-seller.ozon.ru/v2/product/list'
        # marketplace = await Marketplace.get(id=mp).only()
        marketplace = await Marketplace_Pydantic.from_queryset_single(Marketplace.get(id=mp))
        
        headers = {
            'Client-id': marketplace.auth_data['client_id'],
            'Api-Key': marketplace.auth_data['api_key'],
        }

        response = requests.post(host, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        uuid = response.json()

        # print(uuid)

    
        for product in uuid['result']['items']:
            print(product)
            if product['product_id'] not in products:
                product_obj = await Product.create(
                    mp_product_id=product['product_id'],
                    marketplace_id=mp,
                    user_id=user_id
                )
                await product_obj.save()

            
        


