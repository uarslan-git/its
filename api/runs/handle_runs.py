from fastapi import APIRouter
from runs.schemas import Run_code_submission, Evaluated_run_code_submission
from db.db_connector_beanie import User
from db import database
from fastapi import Depends
from users.handle_users import current_active_user
import ast
from submissions.handle_submissions import check_user_code, run_with_timeout
#TODO: secure this:
import sys as unsafe_sys_import 
from io import StringIO

router = APIRouter()

def capture_output(code):
    # Redirect stdout to capture the output
    original_stdout = unsafe_sys_import.stdout
    unsafe_sys_import.stdout = StringIO()
    exec(code)
    # Get the captured output
    output = unsafe_sys_import.stdout.getvalue()
    unsafe_sys_import.stdout = original_stdout
    return output

def parse_argument_types(arg_dict):
    run_arguments = [(key, arg_dict[key]) for key in arg_dict.keys()]
    try:
        check_list = [check_user_code(entry[1]) for entry in run_arguments]
    except Exception as e: 
        return {}, "Illegal argument"
    else:
        try:
            run_arguments= dict([(entry[0], eval(entry[1])) for entry in run_arguments])
        except BaseException as e:
            return {}, "Invalid argument"
        return run_arguments, "Success"


@router.post("/run_code")
async def run_code(submission: Run_code_submission, user: User = Depends(current_active_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    task_type = task_json.type
    if task_type == "function":
        #run_arguments = [(key, submission.run_arguments[key]) for key in submission.run_arguments.keys()]
        #check_list = [check_user_code(ast.parse(entry[1])) for entry in run_arguments]
        #if False in check_list: 
        #    run_code = ""
        #else:
        run_arguments, arg_message = parse_argument_types(submission.run_arguments)
        if arg_message == "Success":
            run_code = """{0}{1}
run_result = {2}(**{3})""".format(task_json.prefix, submission.code, task_json.function_name, run_arguments)
        else: 
            run_code = "raise Exception('{0}')".format(arg_message)
    elif task_type == "print":
        run_code = """
code = '''{0}'''
run_result = capture_output(code)""".format(submission.code)
    else:
        raise Exception("Task type not known.")
    if task_json.prefix == "":
        prefix_lines = []
    else:
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
    wrap_execute_code = lambda queue: execute_code(run_code, prefix_lines, queue)
    run_result = run_with_timeout(wrap_execute_code, timeout=4)
    #run_result = execute_code(run_code)
    evaluated_submission = Evaluated_run_code_submission(
        code = submission.code, submission_time=submission.submission_time, run_arguments=submission.run_arguments,
        run_output=str(run_result), task_unique_name=submission.task_unique_name, log=submission.log, type="run", user_id=user_id
    )
    await database.log_code_submission(evaluated_submission)
    return  {"run_id": str(evaluated_submission.id)}

def execute_code(code, prefix_lines, queue):
    global run_result
    try:
        #parsed_ast = ast.parse(run_code)
        save = check_user_code(code, prefix_lines)
        if save:
            exec(code, globals())
    except BaseException as e:
        run_result = f"Error or Exception: {str(e)}"
    queue.put(run_result)
    return(run_result)