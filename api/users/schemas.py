import datetime
from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional
from fastapi_users.db import BeanieBaseUser
from beanie import Document
from pymongo import IndexModel
from pymongo.collation import Collation


class User(BeanieBaseUser, Document):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    rand_subdomain_orders: list
    courses_completed: list
    register_datetime: dict
    settings: dict
    roles: Optional[list] = None
    #estimated_compentency: Optional[list]
    class Settings:
        """Here we are overwriting the settings class from BeanieBaseUser in order to allow for the optional roles field.
        Basically this allows us to exclude roles from the UserCreate schema in order to avoid security breaches.
        """
        keep_nulls = False
        email_collation = Collation("en", strength=2)
        indexes = [
            IndexModel("email", unique=True),
            IndexModel(
                "email", name="case_insensitive_email_index", collation=email_collation
            ),
        ]
    pass

class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: str
    #username: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    rand_subdomain_orders: list
    courses_completed: list
    register_datetime: dict
    settings: dict
    roles: Optional[list] = None
    pass
    #estimated_compentency: Optional[list]



class UserCreate(schemas.BaseUserCreate):
    email: str
    tasks_completed: list
    tasks_attempted: list
    enrolled_courses: list
    rand_subdomain_orders: list
    courses_completed: list
    register_datetime: dict
    settings: dict
    #roles: Optional[list]
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
