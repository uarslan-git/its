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
    courses_completed: list
    register_datetime: dict
    settings: dict
    #estimated_compentency: Optional[list]
    pass

class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    courses_completed: list
    register_datetime: dict
    settings: dict
    pass
    #estimated_compentency: Optional[list]



class UserCreate(schemas.BaseUserCreate):
    email: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    courses_completed: list
    register_datetime: dict
    settings: dict
    pass
    #username: str
    #estimated_compentency: Optional[list]



class UserUpdate(schemas.BaseUserUpdate):
    """This Schema defines how the request body for the user-patch enpoints has to look. 
    Every setting that is modifyable through the profile-page should be part of this schema.
    Other user-fields, that get update during interactions with the system automatically, 
    are directly updated through database calls. This might be an anti-pattern and change
    in later iterations. Potentially all such information should be stored in different
    documents.
    """
    email: str
    register_datetime: dict
    settings: dict
    pass
