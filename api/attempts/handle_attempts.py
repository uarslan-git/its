from fastapi import APIRouter
from fastapi import Depends
from attempts.schemas import Attempt, AttemptState
from users.schemas import User
from users.handle_users import current_active_user
from db import database
from beanie import PydanticObjectId

router = APIRouter(prefix="/attempt")

@router.get("/get_state/{task_unique_name}")
async def get_attempt_state(task_unique_name, user: User = Depends(current_active_user)):
    attempt = await database.find_attempt(task_unique_name, user.id)
    if attempt is None:
        attempt = Attempt(user_id = str(user.id), task_unique_name=task_unique_name, state_log=[])
        await database.create_attempt(attempt)
        tasks_attempted = user.tasks_attempted
        tasks_attempted.append(task_unique_name)
        await database.update_user(user, {"tasks_attempted": tasks_attempted})
    if len(attempt.state_log)==0:
        return({"attempt_id": str(attempt.id), "code": ""})
    else:
        return(attempt.state_log[-1])

@router.post("/log")
async def log_attempt_state(state: AttemptState, user: User = Depends(current_active_user)):
    attempt = await database.get_attempt(state.attempt_id)
    state.id = str(PydanticObjectId())
    if state.dataCollection:
        attempt.state_log.append(state)
    else:
        if len(attempt.state_log) > 0:
            attempt.state_log[-1] = state
        else: 
           attempt.state_log.append(state) 
    await database.update_attempt(attempt)




