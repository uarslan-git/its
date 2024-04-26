
from models.pedagogical.prototype import Prototype_pedagogical_model
from users.schemas import User
from courses.schemas import Course
from db import database

class Model_manager():
    """Since the ITS should be a research platform that incorporates different methods for feedback and task selection, the model manager
    aims to simplify the use of varying implementations of the pedagogical, domain and learner model. 
    """
    
    def __init__(self):
        """In the constructor all variants of models should be registered (and instantiated) for later selection.
        """
        self.prototype = Prototype_pedagogical_model()

    async def pedagogical_model(self, user: User):
        course_unique_name = user.current_course
        course =  await database.get_course(course_unique_name)
        # TODO: Introduce course-settings to decide between Models
        if type(course.curriculum[0]) == list:
            return self.prototype
        else: 
            return self.prototype
    
    #TODO: Maybe that is not necesessary
    async def domain_model(self):
        raise Exception("Not implemented!")
    
    async def learner_model(self):
        raise Exception("Not implemented!")
