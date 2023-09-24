from datetime import date
from typing import Optional


from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    name: str
    description: str
    services: Optional[list] = None

    model_config = ConfigDict(from_attributes=True)



class SGooding(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    class Config:
        from_attributes = True



