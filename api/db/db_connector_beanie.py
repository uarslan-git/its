import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from typing import Optional

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["its_db"]


class User(BeanieBaseUser, Document):
    email: str
    #username: str
    #tasks_completed: list
    #tasks_attempted: list
    #estimated_compentency: Optional[list]
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
