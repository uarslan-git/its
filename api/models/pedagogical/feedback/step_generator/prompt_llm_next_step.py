from models.pedagogical.feedback.step_generator.base import Base_step_generator
from submissions.schemas import Code_submission
from db import database
import aiohttp
import json

class Prompt_llm_step_generator(Base_step_generator):

    async def predict_next_step(self, submission: Code_submission):
        """This implementation of give_feedback uses the ollama API to receive llm-generated next-step feedback.

        Args:
            submission (Code_submission): The users code submission
        """
        #Retrieve task info and create prompt.
        ollama_url = await self.get_ollama_url()
        task_json = await database.get_task(submission.task_unique_name)
        previous_step = task_json.prefix+submission.code
        task = task_json.task
        #TODO: Make querying LLMs a service.
        #Make request and receive/process LLM-answer
        async with aiohttp.ClientSession() as session:
            instruction = self.create_instruction(previous_step, task=task) #TODO: get short version of tasks or differentiate between local and server.
            payload = {
                    #"model": "codellama-nxt",
                    #"model": "codellama:13b",
                    "model": "llama3",
                    "prompt": instruction,
                    "stream": False,
                    "options": {"num_predict": 200,
                                "stop": ["<s>", "</s>", "[INST]", "[/INST]", "<<SYS>>", "<</SYS>>", "[task end]", "<|eot_id|>"]}
                }
            async with session.post(f"{ollama_url}api/generate", json=payload) as response:
                next_step = await response.text()
                next_step = json.loads(next_step)
        return(next_step["response"])
    
    #TODO: Changing settings should happen either more generically or at some different place.
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
                                 inst="Predict a reasonable next step of the student program. It is important to only predict the next step and not the complete solution! Use no additional import statements and no modules that were not imported so far. Also, there should be only the edited code and no further explanations. The reply should be a Markdown code block. The current program state is:", 
                                b_inst="[INST]", e_inst="[/INST]"):
        return f"""<s> {b_inst} {task_ins}\n"{task}"\n{inst}\n{previous_step} {e_inst}\nNext Step:\n"""