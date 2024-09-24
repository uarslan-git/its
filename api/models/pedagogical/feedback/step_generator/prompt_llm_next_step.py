from models.pedagogical.feedback.step_generator.base import Base_step_generator
#from submissions.schemas import Code_submission
from feedback.schemas import Evaluated_feedback_submission
from db import database
#import aiohttp
#import json
from services.language_generation import generate_language

class Prompt_llm_step_generator(Base_step_generator):

    async def predict_next_step(self, submission: Evaluated_feedback_submission):
        """This implementation of give_feedback uses the ollama API to receive llm-generated next-step feedback.

        Args:
            submission (Code_submission): The users code submission
        """
        #Retrieve task info and create prompt.
        task_json = await database.get_task(submission.task_unique_name)
        previous_step = task_json.prefix+submission.code
        example_solution = task_json.prefix+task_json.example_solution
        task = task_json.task
        instruction, system = self.create_instruction(previous_step, task=task, example_solution=example_solution) #TODO: get short version of tasks or differentiate between local and server.
        course_settings = await database.get_course_settings_for_user(submission.user_id, submission.course_unique_name)
        language_generation_model = course_settings["language_generation_model"]
        next_step = await generate_language(instruction, system=system, model=language_generation_model)
        return next_step
    
    def create_instruction(self, previous_step, task_ins="Consider the following programming task:", task="",
                                 inst="Predict a reasonable next step of the student program. It is important to only predict the next step and not the complete solution! Use no additional import statements and no modules that were not imported so far. Also, there should be only the edited code and no further explanations. The reply should be a Markdown code block. Please consider the students coding style and approach to the problem over the example solution when predicting the next step. NEVER disclose the full example solution. The current program state is:", 
                                example_solution="Not provided"):
        #system = """You are a tutor who wants to give hints to students learning programming by providing them with next steps in programming tasks. You want to generate a step as small as possible, so that the student can continue on their own."""
        system = "You are a prediction model for human programming behaviour. You want to give hints to students learning programming by providing them with possible next steps in programming tasks."
        instruction = f"""{task_ins}\n"{task}"\n**Example Solution:**\n{example_solution}\n{inst}\n{previous_step}\n**Next Step:**\n"""
        return instruction, system
    