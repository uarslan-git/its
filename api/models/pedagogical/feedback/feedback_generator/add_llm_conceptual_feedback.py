from models.pedagogical.feedback.feedback_generator.base import Base_feedback_generator
from services.language_generation import generate_language
from submissions.schemas import Code_submission
from db import database

class LLM_conceptual_explanation_generator(Base_feedback_generator):

    async def generate_feedback(self, predicted_step: str, submission: Code_submission):
        task_json = await database.get_task(submission.task_unique_name)
        previous_state = task_json.prefix+submission.code
        task_description = task_json.task
        instruction, system = self.generate_instruction(predicted_step, previous_state, task_description)
        conceptual_explanation = await generate_language(instruction, system=system)
        conceptual_explanation = conceptual_explanation.strip("'").strip().strip("`")
        return predicted_step + "\n" + conceptual_explanation
    
    def generate_instruction(self, predicted_step, previous_state, task_description):
        system = """You are a tutor suporting a student in programming. You are a professional, helpful and kind. 
        You want to provide just enough support, so that the student can continue on their own."""
        instruction = f"""This is a programming task that a student tried to solve: {task_description}.
The current state of the students attempt at the task is: {previous_state}
A prediction model has predicted the following next step: {predicted_step}
Please explain to the student in one or two sentences the key concept they need to arrive from the current state at this particular next step.
Be careful to not reveal the full solution or any further steps.
Adress the student directly.
Explanation: """
        return instruction, system