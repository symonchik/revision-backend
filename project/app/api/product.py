from datetime import date
import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.marketpl import Marketplace, Marketplace_Pydantic, MarketplaceIn_Pydantic
from app.models.user import UserIn_Pydantic, User_Pydantic
from app.aux.security import get_current_user
from app.models.product import Product_Pydantic, ProductIn_Pydantic
from app.aux.marketplace import update_ozon_products_list




router = APIRouter()

@router.get('/healthz')
async def health_check():
    return {"Health": os.getenv('DATABASE_URL')}

@router.post('/update_list')
async def update_products_list(
    current_user: User_Pydantic = Depends(get_current_user)
):
    # mp_list = await Marketplace.get(user_id=current_user.id).all()
    # User_Pydantic.from_queryset(User.all())
    mp_list = await Marketplace_Pydantic.from_queryset(Marketplace.filter(id=current_user.id).all())
    # print(mp_list.model_dump())
    # print(current_user.id)
    if mp_list:
        # print("update")
        await update_ozon_products_list(
            [mp.id for mp in mp_list],
            user_id=current_user.id
        )
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND )
    
    return []

@router.get('/all', response_model=List[Product_Pydantic])
async def get_all_products(
    current_user: User_Pydantic = Depends(get_current_user)
):
    pass

@router.get('/{mp_product_id}', response_model=Product_Pydantic)
async def get_product(mp_product_id: int):
    pass

# @router.post('/update_list')
# async def update_products_list(mp_product_id: int):
#     pass