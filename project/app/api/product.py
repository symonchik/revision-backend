from datetime import date
import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.marketpl import Marketplace, Marketplace_Pydantic, MarketplaceIn_Pydantic
from app.models.user import UserIn_Pydantic, User_Pydantic
from app.aux.security import get_current_user
from app.models.product import (
    Product,
    Product_Pydantic, 
    ProductIn_Pydantic, 
    Purchase, 
    Purchase_Pydantic
)
from app.aux.marketplace import update_ozon_products_list, update_product_purchases


router = APIRouter()

@router.get('/healthz')
async def health_check():
    return {"Health": os.getenv('DATABASE_URL')}

@router.post('/update_list')
async def update_products_list(
    current_user: User_Pydantic = Depends(get_current_user)
):
    mp_list = await Marketplace_Pydantic.from_queryset(Marketplace.filter(id=current_user.id).all())
    if mp_list:
        await update_ozon_products_list(
            [mp.id for mp in mp_list],
            user_id=current_user.id
        )
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND )
    
    return []

@router.get('/all', response_model=List[Any])
async def get_all_products(
    current_user: User_Pydantic = Depends(get_current_user)
):
    res = await Product.filter(user_id=current_user.id).all().values('id', 'name', 'user_id', 'price', 'discount', 'sku')
    # print(res)
    return res

@router.get('/{product_id}', response_model=Any)
async def get_product(
    product_id: int,
    current_user: User_Pydantic = Depends(get_current_user)
):
    prod_obj = await Product.get(id=product_id).values('id', 'name', 'user_id')
    return prod_obj
    print(prod_obj)
    if prod_obj.user_id == current_user.id:
        return prod_obj.model_dump()

@router.get('/purchase/{product_id}', response_model=List[Product_Pydantic])
async def get_poduct_purchases(
    product_id: int,
    current_user: User_Pydantic = Depends(get_current_user)    
):
    prod_dict = await Product.get(id=product_id).values('id', 'name', 'user_id', 'marketplace_id')
    await update_product_purchases(
        user_id=current_user.id,
        product_id=prod_dict['id'],
        marketplaces_id=prod_dict['marketplace_id']
    )
    purchases = await Purchase_Pydantic.from_queryset(Purchase.filter(product_id=product_id).all())
    return purchases
