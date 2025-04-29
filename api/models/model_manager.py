
from models.pedagogical.content_selection.skipping_easy_tasks import Skipping_task_selector
from models.pedagogical.content_selection.first_uncompleted_task import First_uncompleted_task_selector
from models.knowledge_tracing.pfa_model import PFA_Model
from models.pedagogical.prototype import Prototype_pedagogical_model
from models.pedagogical.skipping_tasks_pfa import Skipping_tasks_pfa_pedagogical_model
from models.pedagogical.llm_feedback_textual import LLM_feedback_textual_pedagogical_model
from models.pedagogical.llm_feedback_code import LLM_feedback_code_pedagogical_model
from users.schemas import User
from db import database

from models.pedagogical.group_A_code_base import Group_A_code_base
from models.pedagogical.group_B_textual_base import Group_B_textual_base
from models.pedagogical.group_C_code_skipping import Group_C_code_skipping
from models.pedagogical.group_D_textual_skipping import Group_D_textual_skipping

import warnings

class Model_Manager():
    """Since the ITS should be a research platform that incorporates different methods for feedback and task selection, the model manager
    aims to simplify the use of varying implementations of the pedagogical, domain and learner model. 
    """
    
    def __init__(self):
        """In the constructor all variants of models should be registered (and instantiated) for later selection.
        """
        
        self.pedagogical_models = {
            "prototype": Prototype_pedagogical_model(),
            "skipping_pfa": Skipping_tasks_pfa_pedagogical_model(),
            "prototype_textual_feedback": LLM_feedback_textual_pedagogical_model(),
            "prototype_code_feedback": LLM_feedback_code_pedagogical_model(),
        }
        self.pedagogical_default = self.pedagogical_models["skipping_pfa"]
        
        # TODO instantiate knowledge tracing and selector models here for better performance, but requires more refactoring
        
        self.group_A = Group_A_code_base()
        self.group_B = Group_B_textual_base()
        self.group_C = Group_C_code_skipping()
        self.group_D = Group_D_textual_skipping()

    
    def get_pedagogical_model(self, model_name: str = None):
        if model_name is None:
            return self.pedagogical_default
        try:
            return self.pedagogical_models[model_name]
        except KeyError as e:
            warnings.warn(f"Pedagogical Model '{model_name}' not known, using default.", UserWarning)
            return self.pedagogical_default

    async def get_pedagogical_model_by_user(self, user: User):
        course_unique_name = user.current_course
        course_settings = await database.get_course_settings_for_user(user.id, course_unique_name)
        model_name = course_settings["pedagogical_model"]
        return self.get_pedagogical_model(model_name)
