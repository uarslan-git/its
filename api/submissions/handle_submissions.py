from fastapi import APIRouter
# from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from os import path
import json
import ast

# import motor.motor_asyncio
import db


router = APIRouter()


# run test on submission
class Code_submission(BaseModel):
    task_id: int
    code: str
    log: str

class Tested_code_submission(Code_submission):
    test_results: list

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
    # task_path = path.join(path.dirname(__file__), "../tasks/task_folder")
    # with open("{0}/task_{1}.json".format(task_path, task_id) , "r") as f:
    #     task_json = json.load(f)
    task_json = await db.db.get_task(str(task_id))
    tests = task_json['tests']
    test_results = []
    for test_name in tests.keys():
        test_results.append(get_test_result(test_code=tests[test_name], test_name=test_name, submission_code=submission.code))
    # Log code submit to database
    tested_submission = Tested_code_submission(log = submission.log, task_id = submission.task_id, code = submission.code, test_results= test_results)
    if (submission.log == "True"):
        await db.db.log_code_submission(tested_submission)
    return  {"test_results": test_results}


def get_test_result(test_code, test_name, submission_code):
    run_test_code = """
try:
    {0}()
    result = 1
except AssertionError as e:
    result = 0
    print(e)""".format(test_name)
    test_submission_code = """
{0}

{1}

{2}
    """.format(submission_code, test_code, run_test_code)
    #print(test_submission_code)
    parsed_ast = ast.parse(test_submission_code)
    #exec(test_submission_code, globals())
    global result
    try:
        save = check_submission_code(ast_tree=parsed_ast)
        if save:
            exec(compile(parsed_ast, filename="<parsed_ast>", mode="exec"), globals())
            result_message = "success" if result else "failure"
        return {"test_name": test_name, "status": result, "message": result_message}
    except Exception as e:
        result = 0
        result_message = str(e)
        return {"test_name": test_name, "status": result, "message": result_message}


def check_submission_code(ast_tree):
    class ImportVisitor(ast.NodeVisitor):
        def __init__(self):
            self.found_imports = False

        def visit_Import(self, node):
            self.found_imports = True
            raise Exception("Imports are not allowed in this context.")

        def visit_ImportFrom(self, node):
            self.found_imports = True
            raise Exception("Imports are not allowed in this context.")

    visitor = ImportVisitor()
    visitor.visit(ast_tree)
    return not visitor.found_imports

# def log_code_submission(submission, test_result):
#     client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
#     db = client.its_db
#     db["submission"].insert_one(jsonable_encoder(submission))

# def get_test_result(test_code, test_name, submission_code):
#     run_test_code = """try:  
#     {0}()
#     print("should work")
#     result = 1
# except AssertionError as e:
#     result = 0
#     print(e)""".format(test_name)
#     test_submission_code = """
# {0}

# {1}

# {2}
#     """.format(submission_code, test_code, run_test_code)
#     print(test_submission_code)
#     exec(test_submission_code, globals())
#     result_message = "succsess!" if result else "failure"
#     return {"test_name": test_name, "status": result, "message": result_message}
