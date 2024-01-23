from _ast import Call, Del, Delete, Global, Interactive, Load, Nonlocal, Store, Name
from typing import Any
from fastapi import APIRouter, Depends
import asyncio
from os import path
import ast
from users.handle_users import current_active_user
from db.db_connector_beanie import User
from submissions.schemas import Code_submission, Tested_code_submission
from tasks.schemas import Task
from config import config

from db import database
from sys import __stdout__
import aiohttp
import json

router = APIRouter()


async def execute_code_judge0(code_payload, url=f"http://{config.judge0_host}:2358"):
    """Execute a code snippet in judge0 and wait for the result to return.

    Args:
        code_payload (str): string containing an executable python program
        url (str, optional): Url of the Judge0 server. Defaults to "http://host:2358".

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            #"expected_output": "null",
            "language_id": "10",
            "max_file_size": "1000", #kb
            #"max_processes_and_or_threads": "1",
            "memory_limit": 100000, #kb
            "source_code": code_payload,
            #"stack_limit": "null",
            #"stdin": "null",
            "wall_time_limit": "10", #sec
            "cpu_time_limit": "10", #sec
            "enable_network": "false",
            "redirect_stderr_to_stdout": "true",
            }
        async with session.post(f"{url}/submissions/?base64_encoded=false", data=payload) as response:
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

async def run_tests(task_json, submission):
    tests = task_json.tests
    test_results = []
    valid_solution = True
    for i, test_name in enumerate(tests.keys()):
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
        test_result = await get_test_result(tests[test_name], test_name, task_json.prefix+submission.code, prefix_lines)
        #TODO: After using Judge0, do we need to change this in order to log all timed out submissions?
        if test_result is None:
            submission.type = "timed_out_submission"
            await database.log_code_submission(submission)
            raise asyncio.TimeoutError
        test_results.append(test_result)
        if test_results[i]["status"] == 0:
            valid_solution = False
    return test_results, valid_solution

@router.post("/code_submit")
async def handle_code_submission(submission: Code_submission, user: User = Depends(current_active_user)):
    """Preprocess coda and run a series of test cases on a code submission.

    Args:
        submission (Code_submission): Submission object as defined in schemas.py
    """
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    test_results, valid_solution = await run_tests(task_json, submission)
    """     tests = task_json.tests
    test_results = []
    valid_solution = True
    for i, test_name in enumerate(tests.keys()):
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
        test_result = await get_test_result(tests[test_name], test_name, task_json.prefix+submission.code, prefix_lines)
        if test_result is None:
            submission.type = "timed_out_submission"
            await database.log_code_submission(submission)
            raise asyncio.TimeoutError
        test_results.append(test_result)
        if test_results[i]["status"] == 0:
            valid_solution = False """
    # Log code submit to database
    tested_submission = Tested_code_submission(log = submission.log, 
                                               task_unique_name = submission.task_unique_name, 
                                               code = submission.code,
                                               possible_choices = [],
                                               correct_choices = [],
                                               selected_choices = [],  
                                               test_results = test_results,
                                               user_id=user_id, 
                                               type="submission",
                                               submission_time=submission.submission_time, 
                                               valid_solution=valid_solution)
    #TODO: implement student model for this.
    if valid_solution and (not submission.task_unique_name in user.tasks_completed):
        user.tasks_completed.append(submission.task_unique_name)
        course = await database.get_course(unique_name=user.enrolled_courses[0])
        if course.curriculum == user.tasks_completed:
            if user.enrolled_courses[0] not in user.courses_completed:
                user.courses_completed.append(user.enrolled_courses[0]) #TODO: Unsafe, secure this
        await database.update_user(user, {"courses_completed": user.courses_completed, "tasks_completed": user.tasks_completed})
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await database.log_code_submission(tested_submission)
    return  {"submission_id": str(tested_submission.id)}

@router.post("/mc_submit")
async def handle_mc_submission(submission: Code_submission, user: User = Depends(current_active_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await database.get_task(str(task_id))
    
    test_results = []
    valid_solution = True

    possible_choices = task_json.possible_choices
    correct_choices = task_json.correct_choices
    selected_choices = submission.selected_choices
    choice_explanations = task_json.choice_explanations

    # Check which choices were made
    answers = [element in selected_choices for element in possible_choices]
    # Check which choices are correct
    results = [a == b for a, b in zip(answers, correct_choices)]
    # Check if all choices are correct
    valid_solution = all(results)
    
    success_text = "Test success:" if valid_solution else "Test failure:"
    result_msg = f"{success_text} \n"

    for choice, correct, explanation in zip(possible_choices, results, choice_explanations):
        correct_choice_msg = "correct" if correct else f"incorrect Reason: \n{explanation}"
        result_msg = f"{result_msg}{choice} is {correct_choice_msg}\n\n"

    test_result = {"test_name": "test_for_mc", "status": valid_solution, "message": result_msg}
    test_results.append(test_result)

    # Log code submit to database
    tested_submission = Tested_code_submission(log = submission.log, 
                                               task_unique_name = submission.task_unique_name, 
                                               code = submission.code, 
                                               possible_choices = possible_choices,
                                               correct_choices = correct_choices,
                                               selected_choices = selected_choices, 
                                               test_results = test_results,
                                               user_id=user_id, 
                                               type="submission",
                                               submission_time=submission.submission_time, 
                                               valid_solution=valid_solution)
    #TODO: implement student model for this.
    if valid_solution and (not submission.task_unique_name in user.tasks_completed):
        user.tasks_completed.append(submission.task_unique_name)
        course = await database.get_course(unique_name=user.enrolled_courses[0])
        if course.curriculum == user.tasks_completed:
            if user.enrolled_courses[0] not in user.courses_completed:
                user.courses_completed.append(user.enrolled_courses[0]) #TODO: Unsafe, secure this
        await database.update_user(user, {"courses_completed": user.courses_completed, "tasks_completed": user.tasks_completed})
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await database.log_code_submission(tested_submission)
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
print("##!serialization!##")
print(json.dumps({{'test_message': test_message, 'test_result': test_result}}, default=json_serialize))
print("##!serialization!##")
    """.format(submission_code, test_code, run_test_code, json_serialize)
    try:
        
        save = check_user_code(submission_code, prefix_lines)
        if save:
            result_string = await execute_code_judge0(test_submission_code)
            if "##!serialization!##" in result_string:
                result_string = result_string.split("##!serialization!##")[1]
                result_string = result_string.split("##!serialization!##")[0]
                result_dict = json.loads(result_string)
                test_message = result_dict["test_message"]
                test_result = result_dict["test_result"]
            else:
                test_result = 0
                test_message = result_string
            result_message = "Test success" if test_result else "Test failure:"
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}   
    except BaseException as e:
        test_result = 0
        result_message = "Error or Exception:"
        test_message = str(e)
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}

@router.get("/submission/feedback/{submission_id}")
async def send_feedback(submission_id):
    feedback = await database.get_submission(str(submission_id))
    return(feedback)

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

        def visit_Name(self, node: Name) -> Any:
            bad_func_list = ["exec", "eval", "open", "breakpoint", "callable",
                                 "delattr", "dir", "getattr", "globals",
                                 "hasattr", "help", "id", "input", "locals", 
                                 "memoryview", "property", "setattr", 
                                 "staticmethod", "vars", "__import__"]
            id = node.id
            if id in bad_func_list:
                raise Exception(f"Name {id} is not allowed in this context")
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
