from models.pedagogical.feedback.base import Base_feedback_generator, Base_step_generator
from models.pedagogical.content_selection.base import Base_task_selector


class Base_pedagogical_model():

    step_generator: Base_step_generator
    feedback_generator: Base_feedback_generator
    task_selector: Base_task_selector

    def select_task():
        raise Exception("Not implemented")
    
    def give_feedback():
        raise Exception("Not implemented")