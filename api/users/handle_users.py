from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication import JWTStrategy
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers
from typing import Optional
#from db.db_connector_beanie import User
from users.schemas import User
from db import User, get_user_db, database
from beanie import PydanticObjectId
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
import os
from config import config
import random
import hashlib

"""For Information about fastapi-users and this implementation of it, please refer to
https://fastapi-users.github.io/fastapi-users/12.1/configuration/overview/"""

filedir = os.path.dirname(__file__)

class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    #TODO: Implement reset password and verification and choose some save tokens.
    reset_password_token_secret = os.environ.get("RESET_PWD_SECRET")
    verification_token_secret = os.environ.get("USER_VERIFICATION_SECRET")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        update_dict = {"roles": ["student"]}
        await database.update_user(user, update_dict)
        #TODO: Add hashed email to global account-list and prevent further accounts from being created
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # Send verification request
        user.verification_email

        #https://realpython.com/python-send-email/
        #Plan: 
        #1. Emain based registration. set is_active=False
        #2. Send verification mail. 
        #3. User verifies: set is_active=True
        #3. Send reset token after verification.

        import smtplib, ssl
        import os


        message = f"Hello new User,\nplease veriy your account using the following verification token:\n{token}"     
        
        #TODO: Mail-sending in eigenes Modul auslagern.
        if config.email_enabled == False:
            print(message)
        else:
            password = os.environ.get("EMAIL_PWD")
            port = 465  # For SSL
            host = os.environ.get("EMAIL_HOST") 
            sender = os.environ.get("EMAIL_ADRESS")

            context = ssl.create_default_context()
            #with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(sender, password)
                server.sendmail(
                    sender, "receiver_email", message.as_string()
                )
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        print("User {0} has logged in".format(user.email))

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        reset_token_key = random.randint(1000000, 9000000)
        hashed_email = hashlib.sha256((user.email + str(reset_token_key)).encode("utf-8")).hexdigest()
        update_dict = {"reset_token_key": reset_token_key, "verificaton_email": hashed_email}
        await database.update_user(user, update_dict)
        message=f"""
Dear User,
your account is now activated, this mail contains important information on how to retrieve your account credentials.
Your username is {user.username}.
The key to generate a password-reset-token for your account is {reset_token_key}.
Since it is possible to reset your password with the reset token, please keep this mail save and secure.
Best wishes
The Curious Camel Team
"""
        if config.email_enabled == False:
            print(message)
        else:
            pass

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