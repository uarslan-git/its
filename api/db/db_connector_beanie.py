import motor.motor_asyncio
from courses.schemas import Course
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from typing import Optional
from users.schemas import User
from tasks.schemas import Task
from attempts.schemas import Attempt
from submissions.schemas import Code_submission as Submission
from runs.schemas import Evaluated_run_code_submission as Run_submission
from tasks.schemas import Task
from feedback.schemas import Evaluated_feedback_submission as Feedback_submission
from schemas import Settings
from beanie import PydanticObjectId


async def get_user_db():
    yield BeanieUserDatabase(User)

class database():
    
    def __init__(self, database_host: str, database_user: str, database_pwd: str, database_port: str=27017) -> None:
        #mo
        DATABASE_URL = f"mongodb://{database_user}:{database_pwd}@{database_host}:{database_port}/?authSource=admin"
        #DATABASE_URL = f"mongodb://{database_host}:27017"
        client = motor.motor_asyncio.AsyncIOMotorClient(
            DATABASE_URL, uuidRepresentation="standard"
        )
        self.db = client["its_db"]

    async def log_code_submission(self, tested_submission):
        #Await to enusre the event-loop is not blocked
        #await self.db["submission"].insert_one(jsonable_encoder(tested_submission))
        await tested_submission.insert()

    async def get_task(self, unique_name):
        task = await Task.find_one(Task.unique_name == unique_name)
        return(task)
        #cursor = self.db.tasks.find({"task_id": task_id})
        #task_json = await cursor.to_list(length=1)
        #if len(task_json) == 1:
        #    return(task_json[0])
        #else: 
        #    raise Exception("Multiple Tasks with same ID present")
        
    async def get_submission(self, submission_id):
        submission = await Submission.find_one(Submission.id == PydanticObjectId(submission_id), with_children=True)
        if submission.type == "run":
            submission = await Run_submission.find_one(Run_submission.id == PydanticObjectId(submission_id))
        elif submission.type == "feedback_request":
            submission = await Feedback_submission.find_one(Feedback_submission.id == PydanticObjectId(submission_id))
        return(submission)

    async def get_user(self, user_id): 
        #Use fastapi_users boilerplate indirectly to increase modularity.
        user = await get_user_db.get(user_id)
        return(user)

    async def update_user(self, user: User):
        #await get_user_db().update(user)
        await user.save()

    async def get_course(self, unique_name):
        course = await Course.find_one(Course.unique_name == unique_name)
        return course
    
    async def get_attempt(self, attempt_id):
        attempt = await Attempt.get(PydanticObjectId(attempt_id))
        return attempt

    async def find_attempt(self, task_unique_name, user_id: PydanticObjectId):
        attempt = await Attempt.find_one(Attempt.task_unique_name == task_unique_name, Attempt.user_id == str(user_id))
        return attempt
    
    async def update_attempt(self, attempt: Attempt): 
        await attempt.save()

    async def create_attempt(self, attempt: Attempt): 
        await attempt.insert()

    async def get_settings(self):
        settings = await Settings.find_one()
        return settings

    async def create_settings(self, settings: Settings):
        old_settings = await Settings.find().to_list()
        if len(old_settings) == 0:
            await settings.insert()

    async def update_settings(self, update_dict):
        settings = await self.get_settings()
        await settings.update({"$set": update_dict})