
from sqlalchemy import Integer, String, Column, JSON, ForeignKey, Computed, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
from datetime import date


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(Integer, Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Integer, Computed("date_to - date_from"))

    user = relationship('Users', back_populates='bookings')
    room = relationship('Rooms', back_populates='bookings')


    def __str__(self):
        return f'Booking {self.id}'