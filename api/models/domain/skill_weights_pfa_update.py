from models import model_manager
from courses.schemas import Course

async def update_skill_parameters(course: Course = None, model_name: str = "pfa"):
    return model_manager.learner_models[model_name].update_course_weights(course)