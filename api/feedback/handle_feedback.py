from fastapi.routing import APIRouter
from db import database

router = APIRouter()


@router.get("/feedback/{submission_id}")
async def send_feedback(submission_id):
    feedback = await database.get_submission(str(submission_id))
    return(feedback)
