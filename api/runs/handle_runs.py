from api.courses.schemas import TaskType
from fastapi import APIRouter
from runs.schemas import Run_code_submission, Evaluated_run_code_submission
from db.db_connector_beanie import User
from db import database
from fastapi import Depends
from users.handle_users import current_active_verified_user
from api.models.domain.submissions.submissions import check_user_code, json_serialize, execute_code_judge0
import json
import re

router = APIRouter()

#def capture_output(code):
#    # Redirect stdout to capture the output
#    original_stdout = unsafe_sys_import.stdout
#    unsafe_sys_import.stdout = StringIO()
#    exec(code)
#    # Get the captured output
#    output = unsafe_sys_import.stdout.getvalue()
#    unsafe_sys_import.stdout = original_stdout
#    return output

def parse_argument_types(arg_dict):
    run_arguments = [(key, arg_dict[key]) for key in arg_dict.keys()]
    try:
        check_list = [check_user_code(entry[1]) for entry in run_arguments]
    except Exception as e: 
        return {}, "Illegal argument"
    else:
        try:
            run_argument_string = dict([(entry[0], f'#$eval(##{entry[1]}##)$#') for entry in run_arguments])
            run_argument_string = json.dumps(run_argument_string)
            run_argument_string = run_argument_string.replace('"#$', "")
            run_argument_string = run_argument_string.replace('$#"', "")
            run_argument_string = run_argument_string.replace('##', '"')
        except BaseException as e:
            return {}, "Invalid argument"
        return run_argument_string, "Success"

@router.post("/run_code")
async def run_code(submission: Run_code_submission, user: User = Depends(current_active_verified_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    task_type = task_json.type
    if task_type == TaskType.Function:
        run_arguments, arg_message = parse_argument_types(submission.run_arguments)
        if arg_message == "Success":
            run_code = """{0}{1}
##!user-code-end!##
run_result = {2}(**{3})
import json
{4}
return_dict = {{"run_result": run_result}}
print("##!serialization!##")
print(json.dumps(return_dict, default=json_serialize))
print("##!serialization!##")""".format(task_json.prefix, submission.code, task_json.function_name, run_arguments, json_serialize)
        else:
            run_code = "raise Exception('{0}')".format(arg_message)
    elif task_type == TaskType.Print:
        run_code = """{0}{1}""".format(task_json.prefix, submission.code)
    elif task_type == TaskType.PlotFunction:
        run_arguments, arg_message = parse_argument_types(submission.run_arguments)
        print("REPLACES", task_json, run_arguments)
        run_code = """{0}
    global plt
    global plot_stringIObytes
    {1}
import io
import base64
plot_stringIObytes = io.BytesIO()
run_result = {2}(**{3})
plot_stringIObytes.seek(0)
plot_base64 = base64.b64encode(plot_stringIObytes.read()).decode()
""".format(task_json.prefix, submission.code, task_json.function_name, run_arguments)
        run_code = run_code.replace(".show()", ".savefig(plot_stringIObytes, format='png')")
        print("CODE\n"+run_code)
    else:
        raise Exception(f"Task type \"{task_type}\" not recognized.")
    if task_json.prefix == "":
        prefix_lines = []
    else:
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
    
    # TEMPORARY FIX so plt does not get passed to judge0
    if task_type == 'plot':
        locals = {}
        exec(run_code, globals(), locals)
        print(locals)
        plot_uri = locals['plot_base64']
        run_result = ''
        evaluated_submission = Evaluated_run_code_submission(
            code = submission.code, selected_choices = [], submission_time=submission.submission_time, run_arguments=submission.run_arguments,
            run_output=str(run_result), task_unique_name=submission.task_unique_name, type="run", user_id=user_id, course_unique_name=submission.course_unique_name,
            plot_uri = plot_uri
        )
    # TEMPORARY FIX end
    else: 
        run_result = await execute_code(run_code, prefix_lines)
        evaluated_submission = Evaluated_run_code_submission(
            code = submission.code, selected_choices = [], submission_time=submission.submission_time, run_arguments=submission.run_arguments,
            run_output=str(run_result), task_unique_name=submission.task_unique_name, type="run", user_id=user_id, course_unique_name=submission.course_unique_name
        )
    
    await database.log_code_submission(evaluated_submission)
    return  {"run_id": str(evaluated_submission.id)}

async def execute_code(code, prefix_lines):
    try:
        save = check_user_code(code.split("##!user-code-end!##")[0], prefix_lines)
        if save:
            run_result = await execute_code_judge0(code_payload=code)
    except BaseException as e:
        run_result = f"Error or Exception: {str(e)}"
    if "##!serialization!##" in run_result:
        pattern = r".*?\##!serialization!##(.*?)\##!serialization!##.*"
        parsed_result_string = re.findall(pattern, run_result, re.DOTALL)
        if len(parsed_result_string)==1:
            parsed_result_string = parsed_result_string[0].strip()
        else:
            raise Exception("Bad Judge0 parsing!")
        #run_result = run_result.split("##!serialization!##")[1]
        #run_result = run_result.split("##!serialization!##")[0]
        run_result = json.loads(parsed_result_string)["run_result"]
    return(run_result)
