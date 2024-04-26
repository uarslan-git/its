from fastapi import APIRouter
from fastapi import Depends
from courses.schemas import Course, CourseInfo, CourseEnrollment, CourseSelection
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from random import randrange
import itertools

router = APIRouter(prefix="/course")

@router.get("/get/{course_unique_name}")
async def get_course(course_unique_name, user: User = Depends(current_active_verified_user)) -> Course:
    if course_unique_name not in user.enrolled_courses:

        enrolled_courses = user.enrolled_courses.copy()
        enrolled_courses.append(course_unique_name)
        update_dict = {"enrolled_courses": enrolled_courses}
        await database.update_user(user, update_dict)
        course_enrollment = CourseEnrollment(user_id=str(user.id), username=user.username,
                                             course_unique_name=course_unique_name,
                                             tasks_completed=[], tasks_attempted=[], completed=False,
                                             rand_subdomain_orders=[-1])
        await database.create_course_enrollment(course_enrollment)
    else:
        course_enrollment = await database.get_course_enrollment(user, course_unique_name)

    rand_subdomain_order = course_enrollment.rand_subdomain_orders[0]
    course = await database.get_course(course_unique_name)
    curriculum = course.curriculum
    sub_domains = course.sub_domains
    course_options = course.course_options

    if type(curriculum[0]) == list:
        # TODO: The random sub-domains should be part of an implementation of a pedagogical model
        # Select random index if not already set
        # and update user with new value
        if rand_subdomain_order == -1:
            rand_subdomain_order = randrange(len(course_options))
            update_dict = {"rand_subdomain_orders": [rand_subdomain_order]}
            await database.update_course_enrollment(course_enrollment, update_dict)

        # Get course option from random index
        rand_chosen_option = course_options[rand_subdomain_order]

        # Sort curriculum according to the order in the chosen course option
        sorted_curriculum = [subdomain_tasks for _, subdomain_tasks in sorted(zip(rand_chosen_option, curriculum))]

        # Flatten the sorted curriculum from a list of task lists to a normal list of tasks
        course.curriculum = [item for sublist in sorted_curriculum for item in sublist]
    else:
        pass

    return(course)


@router.get("/info")
async def get_course_info(User = Depends(current_active_verified_user)) -> CourseInfo:
    courses = await database.get_courses()
    course_list = [{"unique_name": course.unique_name, 
                    "display_name": course.display_name,
                     "number_tasks": len(list(itertools.chain(*course.curriculum))),
                      "domain": course.domain } for course in courses]
    course_info = CourseInfo(course_list=course_list)
    return course_info


#TODO: mit payload ausprobieren!
@router.post("/select")
async def select_course(course_selection: CourseSelection, User = Depends(current_active_verified_user)):
    await database.update_user(User, {"current_course": course_selection.course_unique_name})


async def get_course_enrolment():
    #TODO: switch performance-related stuff and user-data related to courses to a new data-item called course_enrolment.
    pass