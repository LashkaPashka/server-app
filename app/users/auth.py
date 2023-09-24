from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime
from app.users.dao import UsersDAO
from pydantic import EmailStr
from app.config import settings
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict):
    encode_to = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=40)
    encode_to.update({'exp': expire})

    encoded_jwt = jwt.encode(
        encode_to, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.get_db_one_or_null(email=email)
    if not(user and verify_password(password, user.hashed_password)):
        return None
    return user