from fastapi import APIRouter
from runs.schemas import Run_code_submission, Evaluated_run_code_submission
from db.db_connector_beanie import User
from db import database
from fastapi import Depends
from users.handle_users import current_active_user
import ast
from submissions.handle_submissions import check_user_code

router = APIRouter()

@router.post("/run_code")
async def run_code(submission: Run_code_submission, user: User = Depends(current_active_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    task_type = task_json.type
    if task_type == "function":
        run_code = """
{0}
run_result = {1}(**{2})""".format(submission.code, task_json.function_name, submission.run_arguments)
    elif task_type == "print":
        pass
    else:
        raise Exception("Task type not known.")
    global run_result
    try:
        parsed_ast = ast.parse(run_code)
        save = check_user_code(ast_tree=parsed_ast)
        if save:
            exec(run_code, globals())
    except BaseException as e:
        run_result = f"Error or Exception: {str(e)}"
    evaluated_submission = Evaluated_run_code_submission(
        code = submission.code, submission_time=submission.submission_time, run_arguments=submission.run_arguments,
        run_output=str(run_result), task_unique_name=submission.task_unique_name, log=submission.log, type="run", user_id=user_id
    )
    await database.log_code_submission(evaluated_submission)
    return  {"run_id": str(evaluated_submission.id)}
