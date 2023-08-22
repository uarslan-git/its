import datetime
from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: str
    #username: str
    #tasks_completed: list
    #tasks_attempted: list
    #estimated_compentency: Optional[list]



class UserCreate(schemas.BaseUserCreate):
    email: str
    pass
    #username: str
    #tasks_completed: list
    #tasks_attempted: list
    #estimated_compentency: Optional[list]



class UserUpdate(schemas.BaseUserUpdate):
    email: str
    pass
    #username: str
    #tasks_completed: list
    #tasks_attempted: list
    #estimated_compentency: Optional[list]
