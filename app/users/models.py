
from sqlalchemy import Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship




class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[int] = mapped_column(String, nullable=False)


    bookings = relationship('Bookings', back_populates='user')


    def __str__(self):
        return f'User {self.email}'