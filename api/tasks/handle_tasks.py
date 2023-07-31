from fastapi import APIRouter
from fastapi import HTTPException

import db

router = APIRouter()

@router.get("/task/{task_id}")
async def read_task(task_id):
    task_json = await db.database.get_task(str(task_id))
    task_description = task_json["task"]
    if task_description == "":
        raise HTTPException(status_code=400, detail="Task not known")
    return({"task_id": task_id, "task": task_description})
