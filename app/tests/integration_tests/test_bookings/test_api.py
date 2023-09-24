import pytest

from httpx import AsyncClient


@pytest.mark.parametrize('room_id, date_from, date_to, booked_rooms, status_code', [
    (4, '2023-09-07', '2023-09-20', 3, 200),
])
async def test_add_get_bookings(room_id, date_from, date_to, booked_rooms, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post('/bookings/add_db', json={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
    })

    assert response.status_code == status_code



