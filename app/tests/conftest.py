import asyncio
import json
from app.main import app as app_fastapi
from httpx import AsyncClient
from sqlalchemy import insert
import pytest
from app.database import Base, engine, async_session_maker
from app.hotels.models import Hotels
from app.users.models import Users
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.config import settings
from datetime import datetime




@pytest.fixture(scope='session', autouse=True)
async def test_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    def get_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    bookings = get_json('bookings')
    hotels = get_json('hotels')
    rooms = get_json('rooms')
    users = get_json('users')


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


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=app_fastapi, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=app_fastapi, base_url='http://test') as ac:
        await ac.post('/authentication/login', json={
            'email': 'artem@example.com',
            'password': 'artem'
        })
        assert ac.cookies['bonds_rafa']
        yield ac