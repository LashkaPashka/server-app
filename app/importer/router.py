from fastapi import APIRouter
from sqlalchemy import insert
from app.bookings.models import Bookings
from app.database import async_session_maker
import json
from datetime import datetime

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

router = APIRouter(
    prefix='/Import',
    tags=['Ипортирование']
)


@router.post('/')
async def import_file_json():
    def get_json(model: str):
        with open(f'app/static/json/{model}.json', encoding='utf-8') as file:
            return json.load(file)

    bookings = get_json('Bookings')
    hotels = get_json('Hotels')
    rooms = get_json('Rooms')
    users = get_json('Users')


    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
        booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')

    async with async_session_maker() as session:
        stmt1 = insert(Hotels).values(hotels)
        stmt2 = insert(Rooms).values(rooms)
        stmt3 = insert(Users).values(users)
        stmt4 = insert(Bookings).values(bookings)

        await session.execute(stmt1)
        await session.execute(stmt2)
        await session.execute(stmt3)
        await session.execute(stmt4)

        await session.commit()