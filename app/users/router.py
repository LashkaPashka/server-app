from fastapi import APIRouter, HTTPException, status, Response
from app.users.schemes import SAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token


router = APIRouter(
    prefix='/authentication',
    tags=['Auth - пользователей']
)


@router.post('/register')
async def register_user(user: SAuth):
    exiting_user = await UsersDAO.get_db_one_or_null(email=user.email)
    if exiting_user:
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(user.password)
    await UsersDAO.add_users(email=user.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('bonds_rafa', access_token, httponly=True)


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('bonds_rafa')
