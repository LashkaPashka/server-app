from app.users.models import Users
from app.dao.basedao import BaseDAO


class UsersDAO(BaseDAO):
    model = Users

