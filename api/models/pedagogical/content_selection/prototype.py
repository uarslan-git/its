from models.pedagogical.content_selection.base import Base_task_selector
from db import database
from users.schemas import User

class Prototype_task_selector(Base_task_selector):

    async def select(user: User):
        user_course_unique_name = user.enrolled_courses[0]
        course = await database.get_course(user_course_unique_name)
        curriculum = course.curriculum
        user_completed_tasks = user.tasks_completed
        uncompleted_tasks = [curriculum_task for curriculum_task in curriculum if curriculum_task not in user_completed_tasks]
        return(uncompleted_tasks[0])
