from models.pedagogical.base import Base_pedagogical_model
from models.pedagogical.content_selection.prototype import Prototype_task_selector
from users.schemas import User

class Prototype_pedagogical_model(Base_pedagogical_model):

    def __init__(self):
        self.task_selector = Prototype_task_selector

    async def select_task(self, user: User):
        return await self.task_selector.select(user)