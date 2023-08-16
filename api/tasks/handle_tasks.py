from fastapi import APIRouter
from fastapi import HTTPException

import db

router = APIRouter()

class Pedagogical_model():

    task_id = 1

    def select_task(self, user_id):
        self.task_id = self.task_id + 1
        return(str(self.task_id))

pedagogical_model = Pedagogical_model()

@router.get("/task/{task_id}")
async def read_task(task_id):
    if task_id =="1":
        pedagogical_model.task_id = 1
    task_json = await db.database.get_task(str(task_id))
    task_description = task_json["task"]
    if task_description == "":
        raise HTTPException(status_code=400, detail="Task not known")
    return({"task_id": task_id, "task": task_description})

@router.get("/task/for_user/{user_id}")
async def get_task_for_user(user_id):
    task_id = pedagogical_model.select_task(user_id=user_id)
    return(await read_task(task_id))

