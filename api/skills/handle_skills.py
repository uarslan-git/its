from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from models import model_manager
from models.pedagogical.skipping_tasks_pfa import Skipping_tasks_pfa_pedagogical_model
from models.pedagogical.content_selection.skipping_easy_tasks import Skipping_task_selector
from models.knowledge_tracing.pfa_model import PFA_Model
from skills.schemas import Skill
from typing import List
import numpy as np

router = APIRouter(prefix="/skills")

# TODO: check if user is involved in the courses every time
@router.get("/{course_unique_name}")
async def get_skills_overview(course_unique_name: str, user: User = Depends(current_active_verified_user)) -> List[Skill]:
    course = await database.get_course(course_unique_name)
    if course == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course with this unique name was found")
    
    course_enrollment = await database.get_course_enrollment(user, course_unique_name)
    if course_enrollment == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not enrolled in the course")
    
    skill_names = course.competencies # TODO: handle courses with no skills or q_matrix (maybe better extract this out of the pfa_model)
    q_matrix = np.array(list(course.q_matrix.values()))


    pedagogical_model: Skipping_tasks_pfa_pedagogical_model = model_manager.get_pedagogical_model("pfa_model") # TODO: check if these 'type casts' hold always
    task_selector: Skipping_task_selector = pedagogical_model.task_selector
    pfa_model: PFA_Model = task_selector.learner_model

    weights = pfa_model.skill_weights
    success_rate, fail_rate = pfa_model.get_sf_rate(course_enrollment) # mybe dont fail when there is no course enrollment and just set both to 0
    

    result = []
    for i, name in enumerate(skill_names):
        value = (weights[i*3] * success_rate[i]
            + weights[i*3+1] * fail_rate[i]
            + weights[i*3+2])
        

        result.append(Skill(name=name, value=value))

    return result

#maybe more somthing like detail instead of reason
@router.get("/{course_unique_name}/{skill_name}/reason")
async def get_reason(course_unique_name: str, skill_name: str, user: User = Depends(current_active_verified_user)):
    course = await database.get_course(course_unique_name)
    if course == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course with this unique name was found")
    
    if course.competencies == None or skill_name not in course.competencies: # TODO: clarify how to deal with missing competencies
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
        detail="No skill with this name was found")
    
    raise NotImplementedError()


@router.get("/{course_unique_name}/{skill_name}/llm_explanation")
async def get_llm_explanation(course_unique_name: str, skill_name: str, user: User = Depends(current_active_verified_user)):
    course = await database.get_course(course_unique_name)
    if course == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course with this unique name was found")
    
    if course.competencies == None or skill_name not in course.competencies: # TODO: clarify how to deal with missing competencies
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No skill with this name was found")
    
    raise NotImplementedError()
