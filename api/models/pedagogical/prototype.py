from models.pedagogical.base import Base_pedagogical_model
from models.pedagogical.content_selection.prototype import Prototype_task_selector
from users.schemas import User
from submissions.schemas import Code_submission
from db import database
import aiohttp
import json

class Prototype_pedagogical_model(Base_pedagogical_model):

    def __init__(self):
        self.task_selector = Prototype_task_selector
        self.feedback_method = "LLM-next-step"
        self.task_summaries = {}

    async def select_task(self, user: User):
        return await self.task_selector.select(user)
    
    async def give_feedback(self, submission: Code_submission):
        """This implementation of give_feedback uses the ollama API to receive llm-generated next-step feedback.

        Args:
            submission (Code_submission): The users code submission
        """
        #Retrieve task info and create prompt.
        ollama_url = await self.get_ollama_url()
        task_json = await database.get_task(submission.task_unique_name)
        previous_step = task_json.prefix+submission.code
        task = task_json.task
        instruction = self.create_instruction(previous_step, task=task)
        #Make request and receive/process LLM-answer
        async with aiohttp.ClientSession() as session:
    #     if submission.task_unique_name not in self.task_summaries.keys():
    #         payload = {
    #             "model": "codellama-7b-nxt",
    #             "prompt": "Please summarize the following programming task one sentence, focussing only on the actual assignment specs:\nTask:\n'{task}'"
    #         }
    #         async with session.post(f"{ollama_url}/api/generate", json=payload) as response:
    #             summary = await response.text()
    #             summary = json.loads(feedback)
    #             self.task_summaries[submission.task_unique_name] = summary
            instruction = self.create_instruction(previous_step, task="Task should be here") #TODO: get short version of tasks or differentiate between local and server.
            payload = {
                    "model": "codellama-nxt",
                    #"model": "codellama:13b",
                    "prompt": instruction,
                    "stream": False,
                    "options": {"num_predict": 100,
                                "stop": ["<s>", "</s>", "[INST]", "[/INST]", "<<SYS>>", "<</SYS>>", "[task end]"]}
                }
            async with session.post(f"{ollama_url}api/generate", json=payload) as response:
                feedback = await response.text()
                feedback = json.loads(feedback)
        return(feedback["response"])
    
    async def set_ollama_url(self, ollama_url):
        await database.update_settings({"olama_url": ollama_url})

    async def get_ollama_url(self):
        settings = await database.get_settings()
        return settings.ollama_url
    
    async def get_feedback_available(self, task_type):
        settings = await database.get_settings()
        if settings.ollama_url == "" or task_type in ["multiple_choice"]:
            return False
        else:
            return True

    
    def create_instruction(self, previous_step, task_ins="Consider the following programming task:", task="",
                                 inst="Predict a reasonable next step of the student program. It is important to only predict the next step and not the complete solution! Also, there should be only the edited code and no further explanations. The reply should be valid Markdown. The current program state is:", 
                                b_inst="[INST]", e_inst="[/INST]"):
        return f"""<s> {b_inst} {task_ins}\n"{task}"\n{inst}\n{previous_step} {e_inst}\nNext Step:\n"""