
from sqlalchemy import Integer, String, Column, JSON, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship




class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)

    bookings = relationship('Bookings', back_populates='room')
    hotels = relationship('Hotels', back_populates='room')


    def __str__(self):
        return f'Room: {self.name}'