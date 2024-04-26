from beanie import Document
class Course(Document):
    curriculum: list
    unique_name: str
    display_name: str
    domain: str
    sub_domains: list
    course_options: list

class CourseInfo(Document):
    course_list: list[dict]

class CourseEnrollment(Document):
    user_id: str
    username: str
    course_unique_name: str
    tasks_completed: list[str]
    tasks_attempted: list[str]
    rand_subdomain_orders: list
    completed: bool

class CourseSelection(Document):
    course_unique_name: str