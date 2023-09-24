from pydantic import BaseModel, ConfigDict
from typing import Optional


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[list] = None
    rooms_quantity: int
    image_id: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)







