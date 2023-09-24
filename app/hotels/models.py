from sqlalchemy import Integer, String, Column, JSON, ForeignKey, Date, Computed
from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship




class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    services: Mapped[str] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)

    room = relationship('Rooms', back_populates='hotels')

    def __str__(self):
        return f'Hotel: {self.name}'
