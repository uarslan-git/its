from fastapi import APIRouter, Depends
from fastapi import HTTPException
from users.schemas import User
from users.handle_users import current_active_user
from models.pedagogical.prototype import Prototype_pedagogical_model


import db


router = APIRouter()


#class Pedagogical_model():
#
#    task_id = 1
#
#    def select_task(self, user_id):
#        self.task_id = self.task_id + 1
#        return(str(self.task_id))

pedagogical_model = Prototype_pedagogical_model()

@router.get("/task/for_user/")
async def get_task_for_user(user: User = Depends(current_active_user)):
    task_unique_name = await pedagogical_model.select_task(user)
    return(await read_task(task_unique_name))


@router.get("/task/by_name/{unique_name}")
async def read_task(unique_name):
    #if task_id =="1":
    #    pedagogical_model.task_id = 1
    task = await db.database.get_task(unique_name)
    task_description = task.task
    if task_description == "":
        raise HTTPException(status_code=400, detail="Task not known")
    return({"unique_name": unique_name, "task": task_description})



