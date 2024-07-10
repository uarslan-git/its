from fastapi.routing import APIRouter
from fastapi import Depends
from feedback.schemas import Feedback_submission, Evaluated_feedback_submission
from db import database
from users.handle_users import current_active_verified_user
from db.db_connector_beanie import User
from submissions.handle_submissions import run_tests
from feedback.schemas import Url

from models import manager

router = APIRouter()


@router.post("/feedback")
async def handle_handle_feedback_request(submission: Feedback_submission, user: User = Depends(current_active_verified_user)):
    """This API-endpoint receives feedback requests from the frontend and uses them to trigger the inner loop of the ITS. 

    Args:
        submission (Feedback_code_submission): A modified Code submission object with feedback-specific fields.
        user (User, optional): The User who requested the feedback. Defaults to Depends(current_active_user).
    """
    # Run tests and check for trivial feedback cases
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    test_results, valid_solution = await run_tests(task_json, submission)
    pedagogical_model = await manager.pedagogical_model(user)
    evaluated_feedback_submission = Evaluated_feedback_submission(task_unique_name = submission.task_unique_name, 
                                                            course_unique_name=submission.course_unique_name,
                                                            code = submission.code,
                                                            possible_choices = [],
                                                            correct_choices = [],
                                                            selected_choices = [],  
                                                            test_results = test_results,
                                                            user_id=user_id, 
                                                            type="feedback_request",
                                                            submission_time=submission.submission_time, 
                                                            valid_solution=valid_solution,
                                                            feedback="",
                                                            feedback_method=pedagogical_model.feedback_method
                                                            )
    if valid_solution:
        feedback = "All tests pass, your solution is most likely correct, you should submit it."
    # Generate feedback with pedagical model
    else:
        feedback = await pedagogical_model.provide_feedback(evaluated_feedback_submission)
    # Store feedback and return ID
    evaluated_feedback_submission.feedback = feedback
    await database.log_code_submission(evaluated_feedback_submission)
    return {"feedback_id": str(evaluated_feedback_submission.id)}