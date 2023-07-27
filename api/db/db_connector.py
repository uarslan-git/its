import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

class database:

    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.its_db

    async def log_code_submission(self, tested_submission):
        #Await to enusre the event-loop is not blocked
        await self.db["submission"].insert_one(jsonable_encoder(tested_submission))

    async def get_task(self, task_id):
        cursor = self.db.tasks.find({"task_id": task_id})
        task_json = await cursor.to_list(length=1)
        if len(task_json) == 1:
            return(task_json[0])
        else: 
            raise Exception("Multiple Tasks with same ID present")