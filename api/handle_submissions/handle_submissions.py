from fastapi import APIRouter
from pydantic import BaseModel
from os import path
import json

router = APIRouter()


# run test on submission
class Code_submission(BaseModel):
    task_id: int
    code: str

# task schema
class task(BaseModel):
    task_id: int
    task_markdown: str
    example_solution: str
    tests: list

@router.post("/code_submit")
async def handle_code_submission(submission: Code_submission):
# TODO: Funktion: (test_eingabe, soll_ausgabe) -> test_feedback
    task_id = submission.task_id
    task_path = path.join(path.dirname(__file__), "../tasks/task_folder")
    #print(task_path)
    with open("{0}/task_{1}.json".format(task_path, task_id) , "r") as f:
        task_json = json.load(f)
    print(task_json.keys())
    tests = task_json['tests']
    test_results = []
    for test_name in tests.keys():
        test_results.append(get_test_result(test_code=tests[test_name], test_name=test_name, submission_code=submission.code))
    return  {"test_results": test_results}


def get_test_result(test_code, test_name, submission_code):
    run_test_code = """try:  
    {0}()
    print("should work")
    result = 1
except AssertionError as e:
    result = 0
    print(e)""".format(test_name)
    test_submission_code = """
{0}

{1}

{2}
    """.format(submission_code, test_code, run_test_code)
    print(test_submission_code)
    exec(test_submission_code, globals())
    result_message = "succsess!" if result else "failure"
    return {"test_name": test_name, "status": result, "message": result_message}
