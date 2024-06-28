from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from courses.schemas import Course, CourseInfo, CourseEnrollment, CourseSelection, CourseSettings
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from random import randrange
import itertools
import numpy as np

router = APIRouter(prefix="/course")

@router.get("/get/{course_unique_name}")
async def get_course(course_unique_name, user: User = Depends(current_active_verified_user)) -> Course:
    course = await database.get_course(course_unique_name)
    if course_unique_name not in user.enrolled_courses:
        enrolled_courses = user.enrolled_courses.copy()
        enrolled_courses.append(course_unique_name)
        course_settings_index = np.where(np.random.multinomial(1, np.array(course.sample_settings)))[0]
        course_enrollment = CourseEnrollment(user_id=str(user.id), username=user.username,
                                             course_unique_name=course_unique_name,
                                             tasks_completed=[], tasks_attempted=[], completed=False,
                                             course_settings_index=int(course_settings_index))
                                             #rand_subdomain_orders=[-1])
        user_update_dict = {"enrolled_courses": enrolled_courses}
        await database.update_user(user, user_update_dict)
        await database.create_course_enrollment(course_enrollment)
    else:
        course_enrollment = await database.get_course_enrollment(user, course_unique_name)
    
    curriculum = course.curriculum
    sub_domains = course.sub_domains
    
    course_settings_index = course_enrollment.course_settings_index
    course_settings = course.course_settings_list[course_settings_index]
    course = override_course_settings(course, course_settings)
    course.course_settings_list = [course_settings]

    if type(curriculum[0]) == list:
        course.curriculum = [task for sub_domain in course.curriculum for task in sub_domain]
    else:
        pass
    return(course)


@router.get("/get_settings/{course_unique_name}")
async def get_course_settings(course_unique_name, user: User = Depends(current_active_verified_user)) -> Course:
    if (not "admin" in user.roles) or ("tutor" in user.roles):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource"
        )
    course = await database.get_course(course_unique_name)
    return course

@router.post("/update_settings")
async def update_course_settings(courseSettings: CourseSettings, user: User = Depends(current_active_verified_user)):
    course = await database.get_course(courseSettings.course_id)
    course.course_settings_list[0] = courseSettings
    await database.update_course(course, {"course_settings_list": course.course_settings_list}) 


def override_course_settings(course: Course, course_settings):
    #TODO: turn the course settings into an object and access values accordingly!
    if not course_settings["curriculum"] is None: 
        course.curriculum = course_settings["curriculum"]
    course.course_settings_list = None
    course.course_settings = course_settings
    return course



@router.get("/info")
async def get_course_info(User = Depends(current_active_verified_user)) -> CourseInfo:
    courses = await database.get_courses()
    course_list = [{"unique_name": course.unique_name, 
                    "display_name": course.display_name,
                     "number_tasks": len(list(itertools.chain(*course.curriculum))),
                      "domain": course.domain } for course in courses]
    course_info = CourseInfo(course_list=course_list)
    return course_info


@router.post("/select")
async def select_course(course_selection: CourseSelection, User = Depends(current_active_verified_user)):
    await database.update_user(User, {"current_course": course_selection.course_unique_name})


async def get_course_enrolment():
    pass