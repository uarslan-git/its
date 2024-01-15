from models.pedagogical.base import Base_pedagogical_model
from models.pedagogical.content_selection.prototype import Prototype_task_selector
from users.schemas import User
from submissions.schemas import Code_submission

class Prototype_pedagogical_model(Base_pedagogical_model):

    def __init__(self):
        self.task_selector = Prototype_task_selector
        self.feedback_method = "LLM-next-step"

    async def select_task(self, user: User):
        return await self.task_selector.select(user)
    
    async def give_feedback(self, submission: Code_submission):
        return("Feedback")