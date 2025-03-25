from fastapi import APIRouter, Depends
from users.handle_users import current_active_verified_user
from db.db_connector_beanie import User
from submissions.schemas import Base_Submission
from api.models.domain.submissions.submissions import handle_submission

from db import database
from sys import __stdout__

router = APIRouter()

@router.post("/submit")
async def submit(submission: Base_Submission, user: User = Depends(current_active_verified_user)):
    try:
        return await handle_submission(submission, user)
    except Exception as e:
        test_result = 500
        exception_type = type(e)
        test_message = str(e)
        # "test_name": test_name
        return {"status": test_result, "message": f"{exception_type}: {test_message}".strip()}
    
@router.get("/submission/feedback/{submission_id}")
async def send_feedback(submission_id):
    print(submission_id, str(submission_id))
    feedback = await database.get_submission(str(submission_id))
    return feedback
