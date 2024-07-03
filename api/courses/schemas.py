from beanie import Document
from typing import Optional


class CourseSettings(Document):
    course_id: str
    feedback_init_time: Optional[int] = None
    feedback_cooldown: Optional[int] = None
    #Override curriculum: should be optional
    #curriculum: Optional[list] = None

class Course(Document):
    curriculum: list
    unique_name: str
    display_name: str
    #TODO: change naming to "topic"
    domain: str
    sub_domains: list
    #course_options: list
    course_settings: Optional[CourseSettings]
    course_settings_list: Optional[list]
    # Use p-array
    sample_settings: list

class CourseInfo(Document):
    course_list: list[dict]

class CourseEnrollment(Document):
    user_id: str
    username: str
    course_unique_name: str
    tasks_completed: list[str]
    tasks_attempted: list[str]
    #rand_subdomain_orders: list
    completed: bool
    course_settings_index: int

class CourseSelection(Document):
    course_unique_name: str