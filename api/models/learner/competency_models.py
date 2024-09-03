from db import database
from tasks.schemas import Task
from users.schemas import User
from users.handle_users import current_active_verified_user
from courses.schemas import Course
import numpy as np
import math

class Task_completion_probability(User, Task):

    async def select(self, user: User):
        course_enrollment = await database.get_course_enrollment(user, user.current_course)
        if course_enrollment.completed:
            return("course completed")
        q_matrix = user.current_course.q_matrix
        skill_weights = np.array(user.current_course.skill_weights)
        user_completed_tasks = course_enrollment.tasks_completed
        user_attempted_tasks = course_enrollment.tasks_attempted
        num_skills = course_enrollment.skills_number
        new_task_skills = q_matrix.get(Task.unique_name)
        #n=4 #with struggle
        n=3 #without struggle
        new_task_skills= np.repeat(new_task_skills, n)

        # Computing previous successes and failures
        s = np.zeros(num_skills)
        f = np.zeros(num_skills)
        for task in user_attempted_tasks:
            task_skills = q_matrix.get(task)
            if (task in user_completed_tasks):
                s = [sum(x) for x in zip(s, task_skills)]
            else:
                f += [sum(x) for x in zip(s, task_skills)]
        new_task_weights = new_task_skills*skill_weights
        logit = 0
        
        for i in num_skills: 
             logit += new_task_weights[n*i]*s[i] + new_task_weights[n*i+1]*f[i] + new_task_weights[n*i+2]

        return 1 / (1 + math.exp(-logit))
