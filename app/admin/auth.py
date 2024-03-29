
from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.users.auth import create_access_token, authenticate_user
from app.users.dependecies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({'sub': str(user.id)})
            request.session.update({'token': access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:

        token = request.session.get("token")
        user = get_current_user(token)

        if not user:
            return RedirectResponse(status_code=401)

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


authentication_backend = AdminAuth(secret_key="...")
