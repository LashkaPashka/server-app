from fastapi import APIRouter
from datetime import date
from app.hotels.models import Hotels
from app.hotels.HotelDao import HotelDao
from app.hotels.schemes import SHotels
from app.config import settings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import asyncio
from redis import asyncio as aioredis



router = APIRouter(
    prefix='/hotels',
    tags=['Hotel']
)


@router.get('/{location}')
#@cache(expire=30)
async def get_data(location: str, date_from: date, date_to: date) -> list[SHotels]:
    #await asyncio.sleep(3)
    stmt = await HotelDao.return_free_hotels(location, date_from, date_to)

    list_result = []
    dic = await HotelDao.get_location(location)
    for i in range(len(dic)):
        result = dict(dic[i])
        result.update({'rooms_left': stmt[i]})
        list_result.append(result)
    return list_result


@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id: int, date_from: date, date_to: date):
    query = await HotelDao.get_rooms(hotel_id, date_from, date_to)
    return query






@router.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")