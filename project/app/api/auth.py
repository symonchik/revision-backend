import os
from typing import List, Type, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from app.models.user import User, User_Pydantic, UserIn_Pydantic, UserToken, UserToken_Pydantic

from passlib.hash import bcrypt

from app.aux.security import SECRET_KEY, authenticate_user, create_verification_token, get_current_user, validate_token
from app.aux.mail import send_mail
from app.models.pydantic import UserPayloadSchema


router = APIRouter()

@router.get('/healthz')
async def health_check():
    return {"Health": os.getenv('DATABASE_URL')}

@router.post('/users')
async def create_user(user: UserPayloadSchema):
    """
    or need to create with basic fields
    """
    user_obj = await User.create(**user.model_dump())
    user_obj.password_hash = bcrypt.hash(user.password_hash)
    await user_obj.save()
    verification_token = await create_verification_token(user_obj)
    # send_mail(user_obj.email, "Activate Account", f'<strong>{verification_token.token}</strong>')
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.post('/users/activate')
async def activate_user(activation_token):
    result = await validate_token(activation_token)
    if result['status_code'] == 200:
        await User.get(user_id=result['user']).update(is_active = True)
        return await User_Pydantic.from_queryset_single(User.get(user_id=result['user']))
    return result


@router.get('/users', response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(User.all())

@router.get('/users/me', response_model=User_Pydantic)
async def get_session_user(user: User_Pydantic = Depends(get_current_user)):
    return user


@router.get('/users/{user_id}' , response_model=User_Pydantic)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.put('/users/{user_id}', response_model=User_Pydantic)
async def update_user(user_id: int, user: UserIn_Pydantic):
    user.password_hash = bcrypt.hash(user.password_hash)
    await User.get(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.delete('/users/{user_id}')
async def delete_user(user_id: int):
    await User.filter(id=user_id).delete()
    return {}

@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.model_dump(), SECRET_KEY)

    return {'access_token': token, 'token_type': 'bearer'}





@router.get("/all-tokens")
async def get_tokens():
    return await UserToken_Pydantic.from_queryset(UserToken.all())
