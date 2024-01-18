from fastapi import APIRouter, Depends
from fastapi import HTTPException
from users.schemas import User
from users.handle_users import current_active_user
from models import manager

import db

router = APIRouter()

@router.get("/task/for_user/")
async def get_task_for_user(user: User = Depends(current_active_user)):
    task_unique_name = await manager.pedagogical_model(user).select_task(user)
    if task_unique_name == "course completed":
        return({"unique_name": "course completed", "task": ""})
    return(await read_task(task_unique_name))


@router.get("/task/by_name/{unique_name}")
async def read_task(unique_name, user: User = Depends(current_active_user)):
    #if task_id =="1":
    #    pedagogical_model.task_id = 1
    task = await db.database.get_task(unique_name)
    task_description = task.task
    if task_description == "":
        raise HTTPException(status_code=400, detail="Task not known")
    return({
        "unique_name": unique_name, 
        "task": task_description, 
        "type": task.type, 
        "prefix": task.prefix, 
        "arguments": task.arguments, 
        "possible_choices": task.possible_choices,
        "feedback_available":  manager.pedagogical_model(user).get_feedback_available(task.type)
    })