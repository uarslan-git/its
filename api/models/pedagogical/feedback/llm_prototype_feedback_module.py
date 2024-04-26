from models.pedagogical.feedback.base import Base_step_feedback_module
from models.pedagogical.feedback.step_generator.prompt_llm_next_step import Prompt_llm_step_generator
from models.pedagogical.feedback.feedback_generator.identity import Identity_feedback_generator
from db import database


class LLM_prototype_feedback_module(Base_step_feedback_module):

    def __init__(self) -> None:
        self.step_generator = Prompt_llm_step_generator()
        self.feedback_generator = Identity_feedback_generator()

    async def get_feedback_available(self, task_type):
        settings = await database.get_settings()
        if settings.ollama_url == "" or task_type in ["multiple_choice"]:
            return False
        else:
            return True