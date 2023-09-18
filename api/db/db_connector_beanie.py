import motor.motor_asyncio
from courses.schemas import Course
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from typing import Optional
from users.schemas import User
from tasks.schemas import Task
from attempts.schemas import Attempt
from submissions.schemas import Tested_code_submission as Submission
from beanie import PydanticObjectId


async def get_user_db():
    yield BeanieUserDatabase(User)

class database():
    
    def __init__(self) -> None:
        DATABASE_URL = "mongodb://mongodb:27017"
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
        submission = await Submission.find_one(Submission.id == PydanticObjectId(submission_id))
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

