from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from models import model_manager
from models.pedagogical.skipping_tasks_pfa import Skipping_tasks_pfa_pedagogical_model
from models.pedagogical.content_selection.skipping_easy_tasks import Skipping_task_selector
from models.knowledge_tracing.pfa_model import PFA_Model
from skills.schemas import SkillOverview, Skill, ReasonDescription, ExplanationDescription
from typing import List
import numpy as np

from datetime import datetime, timedelta, timezone
from dateutil import parser


router = APIRouter(prefix="/skills")

# TODO: check if user is involved in the courses every time
@router.get("/{course_unique_name}")
async def get_skills_overview(course_unique_name: str, user: User = Depends(current_active_verified_user)) -> SkillOverview:
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
    
    skill_names = course.competencies # TODO: (maybe better extract this out of the pfa_model)
    if skill_names == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This course has no skills")

    pedagogical_model: Skipping_tasks_pfa_pedagogical_model = model_manager.get_pedagogical_model("pfa_model") # TODO: check if these 'type casts' hold always
    task_selector: Skipping_task_selector = pedagogical_model.task_selector
    pfa_model: PFA_Model = task_selector.learner_model

    await pfa_model.set_user(user, course) # TODO: this seems like an anti pattern (wouldn't it be much better to create on pfa model per course and always pass the user as a parameter)
    weights = pfa_model.skill_weights

    tested_submissions = await database.get_tested_submissions_per_user_and_course(user.id, course_unique_name)
    split_point_utc = datetime.now(timezone.utc) - timedelta(days=7)
    
    submissions_last_week = []
    older_submissions = []
    for submission in tested_submissions:
        
        # Is stored as text directly from the frontend in the db, format used 'dd.MM.yyyy HH:mm:ss'
        if parser.parse(submission.submission_time["utc"], dayfirst=True).timestamp() > split_point_utc.timestamp():
            submissions_last_week.append(submission) 
        else:
            older_submissions.append(submission)

    success_rate_last_week, fail_rate_last_week = pfa_model.get_sf_rate_based_on_submissions(older_submissions)
    success_rate_gain, fail_rate_gain = pfa_model.get_sf_rate_based_on_submissions(submissions_last_week)
    pfa_model.unset_user()

    success_rate_now = success_rate_last_week + success_rate_gain
    fail_rate_now =  fail_rate_last_week + fail_rate_gain

    result = []
    for i, name in enumerate(skill_names):
        value_last_week = (weights[i*3] * success_rate_last_week[i]
            + weights[i*3+1] * fail_rate_last_week[i]
            + weights[i*3+2])
        value_now = (weights[i*3] * success_rate_now[i]
            + weights[i*3+1] * fail_rate_now[i]
            + weights[i*3+2])

        result.append(Skill(name=name, value=value_last_week, gain = value_now - value_last_week))
        
    return SkillOverview(skill_list=result)

#maybe more somthing like detail instead of reason
@router.get("/{course_unique_name}/{skill_name}/reason")
async def get_reason(course_unique_name: str, skill_name: str, user: User = Depends(current_active_verified_user)):
    course = await database.get_course(course_unique_name)
    if course == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course with this unique name was found")
    
    if course.competencies == None or skill_name not in course.competencies:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No skill with this name was found")
    
    course_enrollment = await database.get_course_enrollment(user, course_unique_name)
    if course_enrollment == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not enrolled in the course")

    skill_index = course.competencies.index(skill_name)
    associated_tasks = []
    for task_name, skill_vector in course.q_matrix.items():
        if skill_vector[skill_index] > 0.5:
            associated_tasks.append(task_name)

    solved_correctly = []
    solved_incorrectly = []
    not_attempted = []
    for task_name in associated_tasks:
        if task_name in course_enrollment.tasks_attempted:
            if task_name in course_enrollment.tasks_completed:
                solved_correctly.append(task_name)
            else:
                solved_incorrectly.append(task_name)
        else:
            not_attempted.append(task_name)
    
    reason = f"""
The estimation of the skill development is provided with help of Performance Factor Analysis based on the performance in the tasks associated with the skill {skill_name}: \n
Solved correctly: {solved_correctly}
Solved incorrectly: {solved_incorrectly}
Not attempted: {not_attempted}"""
    
    return ReasonDescription(reason=reason)


@router.get("/{course_unique_name}/{skill_name}/llm_explanation")
async def get_llm_explanation(course_unique_name: str, skill_name: str, user: User = Depends(current_active_verified_user)):
    course = await database.get_course(course_unique_name)
    if course == None:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course with this unique name was found")
    
    if course.competencies == None or skill_name not in course.competencies:
        raise HTTPException(            
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No skill with this name was found")
    
    raise NotImplementedError()
