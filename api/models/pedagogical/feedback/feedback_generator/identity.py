from models.pedagogical.feedback.feedback_generator.base import Base_feedback_generator
from submissions.schemas import Code_submission

class Identity_feedback_generator(Base_feedback_generator):

    async def generate_feedback(self, predicted_step: str, submission: Code_submission):
        return predicted_step