from courses.schemas import Course
from users.schemas import User

from abc import ABC, abstractmethod

class Base_task_selector(ABC):
    
    @abstractmethod
    async def select(self, user: User, topic: str = None):
        raise NotImplementedError
    
    @staticmethod
    def get_curriculum(course: Course):
        curriculum = course.curriculum
        # Flatten the curriculum from a dict of task lists to a normal list of tasks
        if isinstance(curriculum, list) and isinstance(curriculum[0], list):
            curriculum = [item for sublist in curriculum for item in sublist]
        return curriculum, course.mandatory_curriculum