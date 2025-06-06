from courses.schemas import Course
from tasks.schemas import Task
from users.schemas import User

from abc import ABC, abstractmethod
import numpy as np

class KT_Factor_Analysis_Model_Base(ABC):
    current_user: User
    q_matrix: np.ndarray
    
    @abstractmethod
    def set_user(self, user: User, course: Course = None):
        raise NotImplementedError()
    
    @abstractmethod
    def unset_user(self):
        raise NotImplementedError()
    
    @abstractmethod
    def completion_probability(self, task: Task):
        raise NotImplementedError()
    
    @abstractmethod
    def update_course_weights(self, course: Course = None):
        raise NotImplementedError()
