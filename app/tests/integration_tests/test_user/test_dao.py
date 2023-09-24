import pytest

from app.users.dao import UsersDAO
from httpx import AsyncClient




@pytest.mark.parametrize('ind, email, is_exists', [
    (1, 'test@test.com', True),
    (2, 'artem@example.com', True),
    (3, 'tool', False),
])
async def test_add_user(ind, email, is_exists, ac: AsyncClient):
    response = await UsersDAO.get_db_user(ind)

    if is_exists:
        assert response
        assert response.email == email
    else:
        assert not response


