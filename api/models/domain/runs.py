from models.domain.submissions.judge0_string_builder import getExecutableString_runFunction, getExecutableString_runPrint, getExecutableString_runPlot
from courses.schemas import TaskType
from runs.schemas import Run_code_submission, Evaluated_run_code_submission
from db.db_connector_beanie import User
from db import database
from models.domain.submissions.submissions import check_user_code, execute_code_judge0, process_plt_plot
import json
import re

json_serialize = """
def json_serialize(obj):
    if isinstance(obj, np.ndarray):
        #return obj.tolist()
        return np.array2string(obj)
    return obj
"""

async def run_code(submission: Run_code_submission, user: User):
    user_id = user.id
    task_json = await database.get_task(submission.task_unique_name)
    print("TASK\n", task_json)
    submission_code = task_json.prefix + submission.code
    run_arguments = parse_argument_types(submission.run_arguments)
    if task_json.type == TaskType.Function:
        run_code = getExecutableString_runFunction(submission_code, task_json.function_name, run_arguments)
    elif task_json.type == TaskType.Print:
        run_code = getExecutableString_runPrint(submission_code, task_json.function_name, run_arguments)
    elif task_json.type == TaskType.PlotFunction:
        run_code = getExecutableString_runPlot(submission_code, task_json.function_name, run_arguments)
    else:
        raise ValueError(f"Task type '{task_json.type}' not recognized.")
    
    if task_json.prefix == "": prefix_lines = []
    else: prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
    
    print("CODE\n", run_code)
    safe = check_user_code(submission_code, prefix_lines)
    if not safe: return
    result_json = await execute_code(run_code)
    print("RESULT\n", result_json)
    if task_json.type in [TaskType.Function]:
        run_result = str(result_json["run_result"])
    elif task_json.type in [TaskType.PlotFunction]:
        run_result = process_plt_plot(result_json["plot_args"])
    else:
        run_result = result_json
    
    evaluated_submission = Evaluated_run_code_submission(
        code = submission.code, selected_choices = [], submission_time=submission.submission_time, run_arguments=submission.run_arguments,
        run_output=run_result, task_unique_name=submission.task_unique_name, type="run", user_id=user_id, course_unique_name=submission.course_unique_name
    )
    
    
    await database.log_code_submission(evaluated_submission)
    return  {"run_id": str(evaluated_submission.id)}

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
        except Exception as e:
            raise ValueError("Invalid argument.")
        return run_argument_string

async def execute_code(code):
    run_result = await execute_code_judge0(code_payload=code)
    if "##!serialization!##" in run_result:
        pattern = r".*?\##!serialization!##(.*?)\##!serialization!##.*"
        parsed_result_string = re.findall(pattern, run_result, re.DOTALL)
        if len(parsed_result_string)==1:
            parsed_result_string = parsed_result_string[0].strip()
        else:
            raise Exception("Bad Judge0 parsing!")
        #run_result = run_result.split("##!serialization!##")[1]
        #run_result = run_result.split("##!serialization!##")[0]
        run_result = json.loads(parsed_result_string)
    return(run_result)
