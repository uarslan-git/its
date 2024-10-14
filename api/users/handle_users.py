from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication import JWTStrategy
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, exceptions
from typing import Optional
#from db.db_connector_beanie import User
from users.schemas import User, GlobalAccountList
from db import User, get_user_db, database
from beanie import PydanticObjectId
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
import os
from config import config
import random
import hashlib
from services.email_sending import send_mail
import re

"""For Information about fastapi-users and this implementation of it, please refer to
https://fastapi-users.github.io/fastapi-users/12.1/configuration/overview/"""

filedir = os.path.dirname(__file__)

class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = os.environ.get("RESET_PWD_SECRET")
    verification_token_secret = os.environ.get("USER_VERIFICATION_SECRET")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        update_dict = {"roles": ["student"]}
        await database.update_user(user, update_dict)
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        verification_email = request._json["verificationEmail"]
        reset_token_key = request._json["resetKey"]
        verification_hash = hashlib.sha256((verification_email + str(reset_token_key)).encode("utf-8")).hexdigest()
        if user.verification_email == verification_hash:
            send_mail(f"""Dear User,

someone has requested to change the password of your account.
Please use the following reset-token to generate a new password.
{token}
""", "ITS password change request", verification_email)
        
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        message = f"Hello {user.username},\n\nplease veriy your account using the following verification token:\n\n{token}"     
        send_mail(message, "ITS user verification" ,user.verification_email)
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        print("User {0} has logged in".format(user.email))

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        reset_token_key = random.randint(10000000, 90000000)
        #Only the hashed concatenation of email+reset_token_key is stored, so that users real identities stay unknown to the admins.
        hashed_email = hashlib.sha256((user.verification_email + str(reset_token_key)).encode("utf-8")).hexdigest()
        message=f"""Dear User,

your account is now activated, this mail contains important information on how to retrieve your account credentials.
Your username is {user.username}.
The key to generate a password-reset-token for your account is {reset_token_key}.
Since it is possible to reset your password with the reset token, please keep this mail save and secure.
"""
        send_mail(message, "ITS account activated with recovery token", user.verification_email)

        global_accounts_list = await database.get_global_accounts_list()
        hashed_email = hashlib.sha256((user.verification_email).encode("utf-8")).hexdigest()
        global_accounts_list.hashed_email_list.append(hashed_email)
        await database.update_global_accounts_list({"hashed_email_list": global_accounts_list.hashed_email_list})

        update_dict = {"verification_email": hashed_email}
        await database.update_user(user, update_dict)

    #Create has to be ovewritten in order to allow for checking for dublicate users based on hashed emails
    async def create(self, user_create, safe: bool = False, request: Optional[Request] = None):
        global_accounts_list = await database.get_global_accounts_list()
        hashed_emails = global_accounts_list.hashed_email_list
        hashed_user_email = hashlib.sha256((user_create.verification_email).encode("utf-8")).hexdigest()
        if hashed_user_email in hashed_emails:
            raise exceptions.UserAlreadyExists()
        settings = await database.get_settings()
        allowed_mail_adress = False
        for regex in settings.email_whitelist:
            if re.match(regex, user_create.verification_email):
                allowed_mail_adress = True
        class EmailDomainNotAllowedException(exceptions.FastAPIUsersException):
            pass
        if not allowed_mail_adress:
            send_mail("Dear User,\n\nan account using this email-adress already exists. Please try to recover it or contact your admin.\n",
                        "ITS Account already exists",
                      user_create.verification_email)
            raise EmailDomainNotAllowedException
        return await BaseUserManager.create(self, user_create, safe, request)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

cookie_transport = CookieTransport(cookie_max_age=7200, cookie_secure=True, cookie_samesite='none', cookie_httponly=False)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=os.environ.get("JWT_SECRET"), lifetime_seconds=7200)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)