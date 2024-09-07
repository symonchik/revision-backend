from datetime import date
import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.marketpl import Marketplace, Marketplace_Pydantic, MarketplaceIn_Pydantic
from app.models.user import UserIn_Pydantic, User_Pydantic
# from app.aux.models import User
# from app.aux.models import User
from app.aux.security import get_current_user


router = APIRouter()

@router.get("/healtz")
async def health_check():
    return {"Health": os.getenv('DATABASE_URL')}

@router.post('/add_ozon')
async def add_ozon_parketplace(
     ozon_mp: MarketplaceIn_Pydantic,
     current_user: User_Pydantic = Depends(get_current_user)
):
     """
     нужно ли как то понимать, что за пользователь зарегался, или это
     нужно на фронет делать?
     """
     ozon_obj = await Marketplace.create(
          mp_name=ozon_mp.mp_name,
          auth_data=ozon_mp.auth_data,
          user_id=current_user.id
     )
     
     await ozon_obj.save()
     return await Marketplace_Pydantic.from_tortoise_orm(ozon_obj)

@router.get("/all", response_model=List[Marketplace_Pydantic])
async def get_all_marketplaces(
     current_user: User_Pydantic = Depends(get_current_user)
):
     return await Marketplace_Pydantic.from_queryset(Marketplace.all())

@router.put("/{mp_id}")
async def update_marketplace(
     mp_id: int,
     new_mp: MarketplaceIn_Pydantic,
     current_user: User_Pydantic = Depends(get_current_user),

):
     mp_to_update = await Marketplace.get(id=mp_id).only()
     if mp_to_update.user_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
     
     await Marketplace.get(id=mp_id).update(**new_mp.dict(exclude_unset=True))
     return await Marketplace_Pydantic.from_queryset_single(Marketplace.get(id=mp_id))

@router.delete('/{mp_id}')
async def delete_user(mp_id: int):
    await Marketplace.filter(id=mp_id).delete()
    return {}