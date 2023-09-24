import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('horo1@gmail.com', 'root', 200),
    ('horo1@gmail.com', 'root1', 409),
    ('abc', 'root', 422)

])
async def test_register(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/authentication/register', json={
        'email': email,
        'password': password
    })

    print(response)
    assert response.status_code == status_code



@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
    ('artem@example.com', 'artem', 200),
])
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/authentication/login', json={
        'email': email,
        'password': password
    })

    assert response.status_code == status_code
