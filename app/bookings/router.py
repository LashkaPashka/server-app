from fastapi import APIRouter, Depends, HTTPException, status
from app.bookings.dao import BookingDao
from app.bookings.schemes import SGooding
from app.users.models import Users
from app.users.dependecies import get_current_user
from pydantic import TypeAdapter
from fastapi_versioning import version

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import asyncio
from app.tasks.tasks import send_email



router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)


@router.get('/get_db')
#@cache(expire=30)
@version(1)
async def get_books(user: Users = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    booking = await BookingDao.get_db_one_or_null(user_id=user.id)
    return booking



@router.delete('/delete_db')
@version(1)
async def delete_db(user: Users = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    booking_1 = await BookingDao.get_db_one_or_null(user_id=user.id)

    if not booking_1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Нечего удалять!')

    await BookingDao.delete_bookings(id=booking_1['id'])
    return f'Status 200 код {HTTPException(status_code=status.HTTP_204_NO_CONTENT)}'




@router.post('/add_db')
@version(1)
async def add_books(
        bookings_1: SGooding,
        user: Users = Depends(get_current_user)):
    old_booking = await BookingDao.get_db_one_or_null(user_id=user.id)
    if old_booking:
        raise HTTPException(status_code=305, detail='У вас уже есть бронь')

    bookings = await BookingDao.add_bookings(user.id, bookings_1.room_id, bookings_1.date_from, bookings_1.date_to)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Места закончились')

    booking = TypeAdapter(SGooding).validate_python(bookings).model_dump()

    #send_email.delay(booking, user.email)
    return booking


@router.on_event("shutdown")
def startup():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

