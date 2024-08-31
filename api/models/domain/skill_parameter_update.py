from db import database
from courses.schemas import Course, CourseEnrollment
from users.schemas import User
import numpy as np
from sklearn.linear_model import LogisticRegression

class Skill_parameters_update(Course):
    
    async def select(self, course: Course):

        #get all the task completions and order it for users and time stamps (last submissions available?) call all_course_submissions + correctness

        all_enrolled_users = await database.get_course_enrollment(Course)


        q_matrix = Course.q_matrix
        num_skills = Course.skills_number

        #user_completed_tasks = course_enrollment.tasks_completed
        #user_attempted_tasks = course_enrollment.tasks_attempted

        
        Xlogreg_reg = []#np.zeros((X.shape[0], num_skills*3))
        Ylogreg=[]
        
        for user in all_enrolled_users:
            Xlogreg_reg_user = []
            Ylogreg_user=[]
            s = np.zeros(num_skills)
            f = np.zeros(num_skills)
            for task in user.tasks_attempted:     
                task_skills = q_matrix.get(task)
                new_row= np.zeros(num_skills*3)
                for j in range(num_skills):
                # adding the entry  
                    new_row[3*j + 0] = s[j]
                    new_row[3*j + 1] = f[j]
                    new_row[3*j + 2] = task_skills[j]
                Xlogreg_reg_user.append(new_row) 
                if (task in user.tasks_completed):
                    s = [sum(x) for x in zip(s, task_skills)]
                    Ylogreg_user.append(1)
                else:
                    f += [sum(x) for x in zip(s, task_skills)]
                    Ylogreg_user.append(0)

            Xlogreg_reg.append(Xlogreg_reg_user)
            Ylogreg.append(Ylogreg_user)
            
        
        pfa_model = LogisticRegression(penalty = 'l2', C = 1.0, fit_intercept = False)
        pfa_model.fit(Xlogreg_reg, Ylogreg)

        coefficients = pfa_model.coef_
        Course.skill_weights = coefficients
        return 
