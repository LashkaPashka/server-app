from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels
from app.bookings.models import Bookings

from app.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload


router = APIRouter(
    prefix='/CORS',
    tags=['Проверка']
)

@router.get("/example/no_orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(
                Rooms.__table__.columns,
                Hotels.__table__.columns,
                Bookings.__table__.columns
            )
            .join(Hotels, Rooms.hotel_id == Hotels.id)
            .join(Bookings, Bookings.room_id == Rooms.id)
        )
        res = await session.execute(query)
        res = res.mappings().all()
        return res



@router.get("/example/orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(joinedload(Rooms.hotels))
            .options(selectinload(Rooms.bookings))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res
