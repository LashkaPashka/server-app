from app.dao.basedao import BaseDAO
from app.hotels.models import Hotels
from app.bookings.dao import BookingDao
from datetime import date
from sqlalchemy import select, insert, and_, or_, func, text, Computed
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import engine, async_session_maker


class HotelDao(BaseDAO):
    model = Hotels

    @classmethod
    async def return_free_hotels(
            cls,
            location: str,
            date_from: date,
            date_to: date):

        async with async_session_maker() as session:
            list_rooms = []
            query = select(func.count(Hotels.id)).select_from(Hotels)
            res1 = await session.execute(query)
            res2 = res1.scalar()

            for i in range(1, res2+1):
                bookings_rooms = select(Bookings).where(
                            and_(
                                Rooms.id == i,

                                or_(
                                    and_(Bookings.date_from >= date_from,
                                         Bookings.date_from < date_to),
                                    and_(
                                        Bookings.date_from <= date_from,
                                        Bookings.date_to > date_from
                                    ),
                                )
                            )
                        ).cte('booking_rooms')


                new_rooms = select((Hotels.rooms_quantity - func.count(bookings_rooms.c.room_id)).label("total_rooms")).select_from(Hotels).join(
                bookings_rooms, bookings_rooms.c.room_id == Hotels.id, isouter=True).where(
                        and_(
                        text(f"hotels.location LIKE '%{location}%'"),
                        Hotels.id == i
                        )
                    ).group_by(Hotels.rooms_quantity, bookings_rooms.c.room_id)



                #print(new_rooms.compile(engine, compile_kwargs={"literal_binds": True}))


                result = await session.execute(new_rooms)
                rooms_left = sum(result.scalars().all())

                if rooms_left != 0:
                    list_rooms.append(rooms_left)
        return list_rooms



    @classmethod
    async def get_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            stmt = select('*').select_from(Rooms).where(Rooms.hotel_id == hotel_id)
            res1 = await session.execute(stmt)
            res = res1.mappings().all()
            new_res = []

            for i in range(len(res)):
                bookings_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == res[i]['id'],
    
                        or_(
                            and_(Bookings.date_from >= date_from,
                                 Bookings.date_from < date_to),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            ),
                        )
                    )
                ).cte('booking_rooms')
    
                new_rooms = select(
                    (Rooms.quantity - func.count(bookings_rooms.c.room_id)).label("total_rooms")).select_from(
                    Rooms).join(
                    bookings_rooms, bookings_rooms.c.room_id == Rooms.id, isouter=True).where(Rooms.hotel_id == res[i]['hotel_id']).group_by(Rooms.quantity, bookings_rooms.c.room_id)


                left_rooms = await session.execute(new_rooms)
                left_rooms = sum(left_rooms.scalars().all())

                total_cost = (date_to - date_from) * res[i]['price']

                new_dict_res = dict(res[i])

                new_dict_res.update({'left_rooms': left_rooms, 'total_cost': total_cost})
                new_res.append(new_dict_res.copy())
            return new_res






    @classmethod
    async def get_location(cls, location: str):
        async with async_session_maker() as session:
            stmt = select('*').select_from(Hotels).where(text(f"hotels.location LIKE '%{location}%'"))
            result = await session.execute(stmt)
            return result.mappings().all()