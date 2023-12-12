from _ast import Call, Del, Delete, Global, Interactive, Load, Nonlocal, Store
from typing import Any
from fastapi import APIRouter, Depends
# from fastapi.encoders import jsonable_encoder
import asyncio
from os import path
import ast
from users.handle_users import current_active_user

from db.db_connector_beanie import User
from submissions.schemas import Code_submission, Tested_code_submission
from tasks.schemas import Task

# import motor.motor_asyncio
import db
from sys import __stdout__
import aiohttp
import json

router = APIRouter()


async def execute_code_judge0(code_payload, url="http://localhost:2358"):
    """Execute a code snippet in judge0 and wait for the result to return.

    Args:
        code_payload (str): string containing an executable python program
        url (str, optional): Url of the Judge0 server. Defaults to "http://localhost:2358".

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    #TODO: Ergebnis als BASE64 abfragen, weil sonst ungültige Zeichen zurückkommen können!
    async with aiohttp.ClientSession() as session:
        payload = {
            #"expected_output": "null",
            "language_id": 10,
            #"max_file_size": "null",
            #"max_processes_and_or_threads": "null",
            #"memory_limit": "null",
            "source_code": code_payload,
            #"stack_limit": "null",
            #"stdin": "null",
            #"wall_time_limit": "null"
            }
        async with session.post(f"{url}/submissions", data=payload) as response:
            run_token = await response.text()
            run_token = json.loads(run_token)["token"]
            #run_token = eval(run_token)["token"]
        max_iter = 100
        for i in range(0, max_iter): #max_iter for querying the status
            async with session.get(f"{url}/submissions/{run_token}") as response:
                run_result = await response.text()
                run_result = json.loads(run_result)
                if run_result["status"]["description"] not in ["In Queue"]:
                    #run_result = json.loads(run_result)["stdout"]
                    return run_result["stdout"]
                #run_result = eval(run_result)["stdout"]
                await asyncio.sleep(0.2)
        raise Exception("Code Sandbox status frozen!")

json_serialize = """
def json_serialize(obj):
    if isinstance(obj, np.ndarray):
        #return obj.tolist()
        return np.array2string(obj)
    return obj"""


# task schema
""" class task(BaseModel):
    task_id: int
    task_markdown: str
    example_solution: str
    tests: list """

@router.post("/code_submit")
async def handle_code_submission(submission: Code_submission, user: User = Depends(current_active_user)):
    """Preprocess coda and run a series of test cases on a code submission.

    Args:
        submission (Code_submission): Submission object as defined in schemas.py
    """
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await db.database.get_task(str(task_id))
    tests = task_json.tests
    test_results = []
    valid_solution = True
    for i, test_name in enumerate(tests.keys()):
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
        #wrap_get_test_result = lambda queue: get_test_result(tests[test_name], test_name, task_json.prefix+submission.code, prefix_lines, queue=queue)
        #test_result = run_with_timeout(wrap_get_test_result, 5)
        test_result = await get_test_result(tests[test_name], test_name, task_json.prefix+submission.code, prefix_lines)
        if test_result is None:
            submission.type = "timed_out_submission"
            await db.database.log_code_submission(submission)
            raise asyncio.TimeoutError
        test_results.append(test_result)
        if test_results[i]["status"] == 0:
            valid_solution = False
    # Log code submit to database
    tested_submission = Tested_code_submission(log = submission.log, task_unique_name = submission.task_unique_name, 
                                               code = submission.code, test_results = test_results,
                                               user_id=user_id, type="submission",
                                               submission_time=submission.submission_time, valid_solution=valid_solution)
    #TODO: implement student model for this.
    if valid_solution and (not submission.task_unique_name in user.tasks_completed):
        user.tasks_completed.append(submission.task_unique_name)
        course = await db.database.get_course(unique_name=user.enrolled_courses[0])
        if course.curriculum == user.tasks_completed:
            if user.enrolled_courses[0] not in user.courses_completed:
                user.courses_completed.append(user.enrolled_courses[0]) #TODO: Unsafe, secure this
        await db.database.update_user(user)
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await db.database.log_code_submission(tested_submission)
    return  {"submission_id": str(tested_submission.id)}


async def get_test_result(test_code, test_name, submission_code, prefix_lines):
    """Run a single test case in an isolated environment and output the test.reults as a dict"""
    run_test_code = """
import json
try:
    {0}()
    test_result = 1
    test_message = ""
except AssertionError as e:
    test_result = 0
    test_message = str(e)
    print(e)""".format(test_name)
    ##########################################################
    test_submission_code = """
import sys as unsafe_sys_import
from sys import __stdout__
from io import StringIO
submission_captured_output = StringIO()
unsafe_sys_import.stdout = submission_captured_output
{0}
unsafe_sys_import.stdout = __stdout__
submission_captured_output = submission_captured_output.getvalue().strip()
{1}
{2}
{3}
##!serialization!##
print(json.dumps({{'test_message': test_message, 'test_result': test_result}}, default=json_serialize))
##!serialization!##
    """.format(submission_code, test_code, run_test_code, json_serialize)
    #print(test_submission_code)
    #exec(test_submission_code, globals())
    global test_result
    global test_message
    try:
        
        save = check_user_code(submission_code, prefix_lines)
        if save:
            #exec(compile(parsed_ast, filename="<parsed_ast>", mode="exec"), globals())
            #exec(test_submission_code, globals())
            result_string = await execute_code_judge0(test_submission_code)
            result_dict = json.loads(result_string)
            test_message = result_dict["test_message"]
            test_result = result_dict["test_result"]
            result_message = "Test success" if test_result else "Test failure:"
        #queue.put({"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()})
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}   
    except BaseException as e:
        test_result = 0
        result_message = "Error or Exception:"
        test_message = str(e)
        #queue.put({"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()})
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}


def check_user_code(code, prefix_lines=[]):
    class ImportVisitor(ast.NodeVisitor):
        def __init__(self, prefix_lines: list=[]):
            self.found_imports = False
            self.prefix_lines = prefix_lines

        def visit_Import(self, node):
            if node.lineno not in self.prefix_lines:
                self.found_imports = True # TODO: Can the bool be removed?
                raise Exception("Imports are not allowed in this context.")
            else: 
                self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.lineno not in self.prefix_lines:
                self.found_imports = True
                raise Exception("Imports are not allowed in this context")
            else:
                self.generic_visit(node)
        
        def visit_Interactive(self, node: Interactive):
            if node.lineno in self.prefix_lines:
                raise Exception("Interactive Mode is not allowed")
            else: 
                self.generic_visit(node)
        
        def visit_Delete(self, node: Delete):
            if node.lineno not in self.prefix_lines:
                raise Exception("Deletes are not allowed in this context")
            else:
                self.generic_visit(node)
        
        def visit_Global(self, node: Global):
            if node.lineno not in self.prefix_lines:
                raise Exception("Global Scope is not allowed")
            else:
                self.generic_visit(node)

        def visit_Nonlocal(self, node: Nonlocal):
            if node.lineno not in self.prefix_lines: 
                raise Exception("Nonlocal Scope is not allowed")
            else:
                self.generic_visit(node)
        
        #def visit_Load(self, node: Load) -> Any:
        #    raise Exception("Load not allowed")
        
        #def visit_Store(self, node: Store) -> Any:
        #    raise Exception("Store not allowed")
        
        def visit_Del(self, node: Del) -> Any:
            if node.lineno not in self.prefix_lines:
                raise Exception("Del not allowed")
            else: self.generic_visit(node)
        
        def visit_Call(self, node: Call) -> Any:
            if "id" in node.func._fields:
                func_id = node.func.id
            else:
                func_id = node.func.attr
                #module_id = node.func.value.id
            if func_id == "exec":
                raise Exception("exec() is not allowed in this context")
            if func_id in ["eval", "open", "breakpoint", "callable",
                                 "delattr", "dir", "getattr", "globals",
                                 "hasattr", "help", "id", "input", "locals", 
                                 "memoryview", "property", "setattr", 
                                 "staticmethod", "vars", "__import__"]:
                raise Exception(f"{func_id}() is not allowed in this context")
            self.generic_visit(node)

    ast_tree = ast.parse(code)
    visitor = ImportVisitor(prefix_lines=prefix_lines)
    visitor.visit(ast_tree)
    print(code)
    bad_strings = ["np.distutil", "multiprocessing", "APIRouter", "asyncio", "current_active_user", "unsafe_sys_import", "database", "run_with_timeout"]
    for string in bad_strings:
        if string in code:
            raise Exception("Bad symbol detected, please don't use {0} in your program".format(string))
    return not visitor.found_imports
