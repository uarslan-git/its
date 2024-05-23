from models.pedagogical.feedback.step_generator.base import Base_step_generator
from submissions.schemas import Code_submission
from db import database
#import aiohttp
#import json
from services.language_generation import generate_language

class Prompt_llm_step_generator(Base_step_generator):

    async def predict_next_step(self, submission: Code_submission):
        """This implementation of give_feedback uses the ollama API to receive llm-generated next-step feedback.

        Args:
            submission (Code_submission): The users code submission
        """
        #Retrieve task info and create prompt.
        task_json = await database.get_task(submission.task_unique_name)
        previous_step = task_json.prefix+submission.code
        task = task_json.task
        instruction = self.create_instruction(previous_step, task=task) #TODO: get short version of tasks or differentiate between local and server.
        next_step = await generate_language(instruction, model="llama3")
        return next_step
    
    #TODO: Changing settings should happen either more generically or at some different place.
    #async def set_ollama_url(self, ollama_url):
    #    await database.update_settings({"olama_url": ollama_url})

    
    async def get_feedback_available(self, task_type):
        settings = await database.get_settings()
        if settings.ollama_url == "" or task_type in ["multiple_choice"]:
            return False
        else:
            return True
    
    def create_instruction(self, previous_step, task_ins="Consider the following programming task:", task="",
                                 inst="Predict a reasonable next step of the student program. It is important to only predict the next step and not the complete solution! Use no additional import statements and no modules that were not imported so far. Also, there should be only the edited code and no further explanations. The reply should be a Markdown code block. The current program state is:", 
                                b_inst="[INST]", e_inst="[/INST]"):
        return f"""<s> {b_inst} {task_ins}\n"{task}"\n{inst}\n{previous_step} {e_inst}\nNext Step:\n"""