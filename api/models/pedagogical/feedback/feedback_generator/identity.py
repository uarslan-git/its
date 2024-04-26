from models.pedagogical.feedback.feedback_generator.base import Base_feedback_generator

class Identity_feedback_generator(Base_feedback_generator):

    def generate_feedback(self, predicted_step: str):
        return predicted_step