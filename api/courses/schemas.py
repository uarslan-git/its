from beanie import Document

class Course(Document):
    curriculum: list
    unique_name: str
    display_name: str
    domain: str
    sub_domains: list
    course_options: list