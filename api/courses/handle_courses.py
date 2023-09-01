from fastapi import APIRouter
from fastapi import Depends
from courses.schemas import Course
from users.schemas import User
from users.handle_users import current_active_user
from db import database


router = APIRouter(prefix="/course")

@router.get("/get")
async def get_course(user: User = Depends(current_active_user)):
    course_unique_name = user.enrolled_courses[0]
    course = await database.get_course(course_unique_name)
    return(course)
