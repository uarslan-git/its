from fastapi import APIRouter
from fastapi import Depends
from courses.schemas import Course
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from random import randrange

router = APIRouter(prefix="/course")

@router.get("/get")
async def get_course(user: User = Depends(current_active_verified_user)):
    #TODO: change when users can enrol for multiple courses.
    course_unique_name = user.enrolled_courses[0]
    rand_subdomain_order = user.rand_subdomain_orders[0]

    course = await database.get_course(course_unique_name)
    curriculum = course.curriculum
    sub_domains = course.sub_domains
    course_options = course.course_options

    # Select random index if not already set
    # and update user with new value
    if rand_subdomain_order == -1:
        rand_subdomain_order = randrange(len(course_options))
        update_dict = {"rand_subdomain_orders": [rand_subdomain_order]}
        await database.update_user(user, update_dict)

    # Get course option from random index
    rand_chosen_option = course_options[rand_subdomain_order]

    # Sort curriculum according to the order in the chosen course option
    sorted_curriculum = [subdomain_tasks for _, subdomain_tasks in sorted(zip(rand_chosen_option, curriculum))]

    # Flatten the sorted curriculum from a list of task lists to a normal list of tasks
    course.curriculum = [item for sublist in sorted_curriculum for item in sublist]

    return(course)
