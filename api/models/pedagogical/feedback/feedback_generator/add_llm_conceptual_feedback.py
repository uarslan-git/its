from models.pedagogical.feedback.feedback_generator.base import Base_feedback_generator
from services.language_generation import generate_language
from feedback.schemas import Evaluated_feedback_submission
from db import database

class LLM_conceptual_explanation_generator(Base_feedback_generator):

    def __init__(self, textual_feedback_only: bool = True) -> None:
        super().__init__()
        self.textual_feedback_only = textual_feedback_only

    async def generate_feedback(self, predicted_step: str, submission: Evaluated_feedback_submission):
        task_json = await database.get_task(submission.task_unique_name)
        previous_state = task_json.prefix+submission.code
        task_description = task_json.task
        test_messages = "\n".join([test["message"] for test in submission.test_results])
        instruction, system = self.generate_instruction(predicted_step, previous_state, task_description, test_messages=test_messages)
        course_settings = await database.get_course_settings_for_user(submission.user_id, submission.course_unique_name)
        language_generation_model = course_settings["language_generation_model"]
        conceptual_explanation = await generate_language(instruction, system=system, model=language_generation_model)
        conceptual_explanation = conceptual_explanation.strip("'").strip().strip("`")
        if self.textual_feedback_only: 
            return conceptual_explanation
        else:
            return predicted_step + "\n" + conceptual_explanation
    
    def generate_instruction(self, predicted_step, previous_state, task_description, test_messages):
        system = """You are a tutor suporting a student in programming. You are a professional, helpful and kind. 
        You want to provide just enough support, so that the student can continue on their own."""
        instruction = f"""This is a programming task that a student tried to solve: {task_description}.
The current state of the students attempt at the task is: {previous_state}
A prediction model has predicted the following next step: {predicted_step}
Additionally, you can consider the failure messages from automated unit-tests on the students current state. They can hint at problems in the student code.
But be careful, the unit-test messages can also be incomplete and misleading. The unit test Messages are: {test_messages}
Please explain to the student in one or two sentences the key concept they need to arrive from the current state at this particular next step.
Note that the predicted step is not known by the student as they have not yet taken it. Be careful to not reveal the full solution or any further steps.
Adress the student directly.
**Explanation:** """
        return instruction, system