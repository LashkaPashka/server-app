from app.dao.basedao import BaseDAO
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, async_session_maker
from sqlalchemy import and_, or_, insert, select, func, delete
from datetime import date

from app.logger import logger


class BookingDao(BaseDAO):
    model = Bookings

    @classmethod
    async def add_bookings(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date):
        try:
            async with async_session_maker() as session:
                bookings_rooms = select(Bookings).where(
                    and_(
                        Rooms.id == room_id,

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

                rooms_left = select(Rooms.quantity - func.count(bookings_rooms.c.user_id)).select_from(Rooms).join(
                    bookings_rooms, bookings_rooms.c.room_id == Rooms.id, isouter=True).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, bookings_rooms.c.room_id)

               #print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                result = await session.execute(rooms_left)
                result = result.scalar()



                if result > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price
                    ).returning(Bookings.id,
                                Bookings.user_id,
                                Bookings.room_id,
                                Bookings.date_from,
                                Bookings.date_to)
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    return None
        except (SQLAlchemyError, Exception) as er:
            if isinstance(er, SQLAlchemyError):
                msg = 'Database Exc:'
            elif isinstance(er, Exception):
                msg = 'Unknown Exc:'
            msg += 'Cannot add booking'
            extra = {
                'user_id': user_id,
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to
            }
            logger.error(msg, extra=extra, exc_info=True)


    @classmethod
    async def delete_bookings(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = delete(Bookings).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()



            '''WITH booking_rooms AS(
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-06-08' AND date_from < '2023-06-20') OR
            (date_from <= '2023-06-08' AND date_to > '2023-06-08')
        )
        
        SELECT rooms.quantity - COUNT(booking_rooms.user_id) FROM rooms
        LEFT JOIN booking_rooms ON booking_rooms.user_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY booking_rooms.user_id, rooms.quantity
            '''





