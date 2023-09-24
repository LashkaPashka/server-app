from app.hotels.rooms.models import Rooms
from app.dao.basedao import BaseDAO
from app.bookings.models import Bookings
from app.database import engine, async_session_maker
from sqlalchemy import select, and_, or_, func
from datetime import date
from app.hotels.models import Hotels



class RoomDao(BaseDAO):
    model = Rooms

    @classmethod
    async def get_context(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(Rooms.name, Rooms.description, Rooms.services).select_from(Rooms).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.mappings().one()


    @classmethod
    async def get_list_context(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            pass
            









