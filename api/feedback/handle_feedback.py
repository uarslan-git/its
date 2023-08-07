from fastapi.routing import APIRouter

router = APIRouter()
import db

@router.get("/feedback/{submission_id}")
async def send_feedback(submission_id):
    feedback_json = await db.database.get_feedback(str(submission_id))
    return(feedback_json)