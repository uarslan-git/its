from fastapi import APIRouter
from fastapi import Depends
from attempts.schemas import Attempt, AttemptState
from users.schemas import User
from users.handle_users import current_active_user
from db import database
from beanie.exceptions import CollectionWasNotInitialized

router = APIRouter(prefix="/attempt")

@router.get("/get_state/{task_unique_name}")
async def get_attempt_state(task_unique_name, user: User = Depends(current_active_user)):
    attempt = await database.find_attempt(task_unique_name, user.id)
    if attempt is None:
        attempt = Attempt(user_id = str(user.id), task_unique_name=task_unique_name, state_log=[])
        await database.create_attempt(attempt)
        return({"attempt_id": str(attempt.id), "code": ""})
    else: #TODO: was passiert wenn state_log leer ist?
        return(attempt.state_log[-1])


@router.post("/log")
async def log_attempt_state(state: AttemptState, user: User = Depends(current_active_user)):
    attempt = await database.get_attempt(state.attempt_id)
    attempt.state_log.append(state)
    await database.update_attempt(attempt)