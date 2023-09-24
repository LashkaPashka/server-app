from sqladmin import Admin, ModelView
from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels



class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    name = "User"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c]
    name = "Booking"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
    can_delete = False


class RoomAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c]
    name = "Room"
    name_plural = "Комнаты"
    icon = "fa-solid fa-door-open"
    can_delete = False


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    name = "Hotel"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
    can_delete = False


