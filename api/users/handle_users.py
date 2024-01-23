from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication import JWTStrategy
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers
from typing import Optional
from db.db_connector_beanie import User
from db import User, get_user_db, database
from beanie import PydanticObjectId
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
import os

"""For Information about fastapi-users and this implementation of it, please refer to
https://fastapi-users.github.io/fastapi-users/12.1/configuration/overview/"""

filedir = os.path.dirname(__file__)
with open(os.path.join(filedir,"SECRET.txt")) as f:
    SECRET = f.readline()

class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    #TODO: Implement reset password and verification and choose some save tokens.
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        user.roles = ["student"]
        await database.update_user(user)
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        print("User {0} has logged in".format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(cookie_max_age=7200, cookie_secure=True, cookie_samesite='none', cookie_httponly=False)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=7200)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

#fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])
fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])


current_active_user = fastapi_users.current_user(active=True)
