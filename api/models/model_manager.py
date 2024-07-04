
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
        self.default = Prototype_pedagogical_model()

    async def pedagogical_model(self, user: User):
        course_unique_name = user.current_course
        course_settings = await database.get_course_settings_for_user(user.id, course_unique_name)
        model_name = course_settings["pedagogical_model"]
        if model_name is None:
            return self.default
        try:
            return getattr(self, model_name)
        except AttributeError as e:
            print("Warning: Pedagogical Model {model_name} not known, using default.")
            return self.default
    
    async def domain_model(self):
        raise Exception("Not implemented!")
    
    async def learner_model(self):
        raise Exception("Not implemented!")
