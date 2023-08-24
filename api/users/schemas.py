import datetime
from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional
from fastapi_users.db import BeanieBaseUser
from beanie import Document


class User(BeanieBaseUser, Document):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    #estimated_compentency: Optional[list]
    pass

class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    pass
    #estimated_compentency: Optional[list]



class UserCreate(schemas.BaseUserCreate):
    email: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    pass
    #username: str
    #estimated_compentency: Optional[list]



class UserUpdate(schemas.BaseUserUpdate):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    #estimated_compentency: Optional[list]
    pass
