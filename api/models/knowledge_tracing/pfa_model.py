import warnings
from models.knowledge_tracing.kt_base import KT_Factor_Analysis_Model_Base
from courses.schemas import Course
from tasks.schemas import Task
from users.schemas import User
from db import database

from sklearn.linear_model import LogisticRegression
import numpy as np
from collections.abc import Iterable
from submissions.schemas import Tested_Submission


class PFA_Model(KT_Factor_Analysis_Model_Base):
    current_user: User
    q_matrix: dict
    competencies: list
    skill_weights: np.ndarray
    succ_rate: np.ndarray
    fail_rate: np.ndarray
    
    def __init__(self, n_parameters: int = 3):
        self.n = n_parameters
        super().__init__()
    
    async def set_user(self, user: User, course: Course = None):
        self.current_user = user
        if course == None:
            course = await database.get_course(user.current_course)
        course_enrollment = await database.get_course_enrollment(user, course.unique_name)

        # set default values if any are not present
        if (course.q_matrix == None or
            course.competencies == None or
            course.course_parameters == None or
            not "skill_weights_pfa" in course.course_parameters.keys()):
            await self.set_default_q_matrix(course, self.n)
        self.q_matrix = course.q_matrix
        self.competencies = course.competencies
        self.skill_weights = np.array(course.course_parameters.get("skill_weights_pfa"))
        
        self.succ_rate, self.fail_rate = self.get_sf_rate(course_enrollment)
        return self

    def unset_user(self):
        self.current_user = None
        self.q_matrix = None
        self.competencies = None
        self.skill_weights = None
        self.succ_rate = None
        self.fail_rate = None
    
    def completion_probability(self, task: Task):
        if self.current_user == None:
            raise AttributeError("PFA Model has not been set to a user. Call 'set_user' before calculating completion probability.")
        
        new_task_skills = self.q_matrix.get(task)
        new_task_skills = np.repeat(new_task_skills, self.n)
        new_task_weights = new_task_skills * self.skill_weights

        logit = 0
        for i in range(len(self.competencies)):
            logit += new_task_weights[self.n*i]*self.succ_rate[i]
            + new_task_weights[self.n*i+1]*self.fail_rate[i]
            + new_task_weights[self.n*i+2]
        return 1 / (1 + np.exp(-logit))
        
    async def update_course_weights(self, courses: list[Course]):
        if not courses:
            return

        Xlogreg_reg = []
        Ylogreg = []
        
        all_skills = []
        for course in courses:
            all_skills.extend(course.competencies)
        all_skills = sorted(list(set(all_skills)))

        for course in courses:
            all_enrolled_users = await database.get_all_enrolled_users(course.unique_name)
            q_matrix = course.q_matrix
            num_skills = len(course.competencies)

            for user_enrollment in all_enrolled_users:
                s = np.zeros(len(all_skills))
                f = np.zeros(len(all_skills))
                for task in user_enrollment.tasks_attempted:
                    if task in q_matrix:
                        task_skills_original = q_matrix.get(task)
                        task_skills_mapped = np.zeros(len(all_skills))
                        for i, skill in enumerate(course.competencies):
                            if skill in all_skills:
                                skill_index = all_skills.index(skill)
                                task_skills_mapped[skill_index] = task_skills_original[i]

                        new_row = np.zeros(len(all_skills) * self.n)
                        for j in range(len(all_skills)):
                            new_row[3*j + 0] = s[j]
                            new_row[3*j + 1] = f[j]
                            new_row[3*j + 2] = task_skills_mapped[j]
                        
                        if (task in user_enrollment.tasks_completed):
                            s = [sum(x) for x in zip(s, task_skills_mapped)]
                            Ylogreg.append(1)
                        else:
                            f += [sum(x) for x in zip(f, task_skills_mapped)]
                            Ylogreg.append(0)
                        Xlogreg_reg.append(new_row)

        if not Xlogreg_reg or len(set(Ylogreg)) < 2:
            return
        
        pfa_model = LogisticRegression(penalty = 'l2', C = 1.0, fit_intercept = False)
        pfa_model.fit(Xlogreg_reg, Ylogreg)

        coefficients = (-pfa_model.coef_[0]).tolist()
        
        for course in courses:
            course_parameters_new = course.course_parameters.copy()
            skill_weights_pfa = np.zeros(len(course.competencies) * self.n)
            for i, skill in enumerate(course.competencies):
                if skill in all_skills:
                    skill_index = all_skills.index(skill)
                    skill_weights_pfa[i*self.n:(i+1)*self.n] = coefficients[skill_index*self.n:(skill_index+1)*self.n]
            
            course_parameters_new["skill_weights_pfa"] = skill_weights_pfa.tolist()
            await database.update_course(course, {"course_parameters": course_parameters_new})

    def get_sf_rate(self, course_enrollment):
        attempted_tasks = course_enrollment.tasks_attempted
        completed_tasks = course_enrollment.tasks_completed
        
        succ_rate = np.zeros(len(self.competencies))
        fail_rate = np.zeros(len(self.competencies))
        for task in attempted_tasks:
            if task in completed_tasks:
                succ_rate = np.add(succ_rate, self.q_matrix.get(task))
            else:
                fail_rate = np.add(fail_rate, self.q_matrix.get(task))
        return succ_rate, fail_rate
    
    def get_sf_rate_based_on_submissions(self, tested_submissions : Iterable[Tested_Submission]):
        succ_rate = np.zeros(len(self.competencies))
        fail_rate = np.zeros(len(self.competencies))

        for tested_submission in tested_submissions:
            if tested_submission.valid_solution:
                succ_rate += self.q_matrix.get(tested_submission.task_unique_name)
            else:
                fail_rate += self.q_matrix.get(tested_submission.task_unique_name)
        return succ_rate, fail_rate
        

    @staticmethod
    async def set_default_q_matrix(course: Course, n_parameters: int):
        warnings.warn(f"PFA: Some required fields not found for course '{course.unique_name}' not found, constructing default Q-Matrix.")
        
        competencies = ["default_competency"]
        q_matrix = {task: [1] for task in course.curriculum}
        course_parameters = course.course_parameters
        
        skill_weights_pfa = [0] * n_parameters
        if course_parameters == None:
            course_parameters = {"skill_weights_pfa": skill_weights_pfa}
        else:
            course_parameters["skill_weights_pfa"] = skill_weights_pfa
        
        await database.update_course(course, {
            "q_matrix": q_matrix,
            "competencies": competencies,
            "course_parameters": course_parameters,})