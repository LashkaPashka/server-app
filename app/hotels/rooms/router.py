from app.hotels.router import router
from datetime import date


@router.get('/{hotel_id}/rooms')
async def get_list_rooms(hotel_id: int, date_from: date, date_to: date):
    pass






