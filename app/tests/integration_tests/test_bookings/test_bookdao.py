import pytest
from datetime import datetime

from app.bookings.dao import BookingDao


@pytest.mark.parametrize('user_id, room_id', [
    (1, 2),
    (2, 3),
])
async def test_add_bookings(user_id, room_id):
    new_bookings = await BookingDao.add_bookings(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime('2023-08-06', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-08-20',  '%Y-%m-%d'),
    )

    assert new_bookings['user_id'] == user_id
    assert new_bookings['room_id'] == room_id




@pytest.mark.parametrize('user_id, bookings_rooms', [
    (1, 3)
])
async def test_get_bookings(user_id, bookings_rooms):
    new_bookings = await BookingDao.get_db_all(user_id=user_id)

    assert len(new_bookings) == bookings_rooms

    delete_bookings = await BookingDao.delete_bookings(user_id=user_id)

    new_bookings = await BookingDao.get_db_all(user_id=user_id)
    assert not new_bookings

