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

import multiprocessing

# import motor.motor_asyncio
import db
from io import StringIO
#TODO: Discuss how this can be prohibited!
import sys as unsafe_sys_import
from sys import __stdout__

router = APIRouter()

def run_with_timeout(func, timeout):
    # Create a multiprocessing Queue for communication
    result_queue = multiprocessing.Queue()

    # Create a multiprocessing Process
    process = multiprocessing.Process(target=func, args=(result_queue,))

    try:
        # Start the process
        process.start()

        # Wait for the process to finish or timeout
        process.join(timeout)

        # If the process is still alive, terminate it
        if process.is_alive():
            #active = multiprocessing.active_children()
            #for child in active: 
            #    child.terminate()
            #    child.kill()
            process.terminate()
            process.kill()
            process.join()
            print("Process terminated due to timeout.")
        else:
            # Get the result value after the process has finished
            result = result_queue.get(timeout=1)
            print(f"Process completed within the timeout. Result: {result}")
            return(result)
    except Exception as e:
        print(f"An error occurred: {e}")

# task schema
""" class task(BaseModel):
    task_id: int
    task_markdown: str
    example_solution: str
    tests: list """

@router.post("/code_submit")
async def handle_code_submission(submission: Code_submission, user: User = Depends(current_active_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await db.database.get_task(str(task_id))
    tests = task_json.tests
    test_results = []
    valid_solution = True
    for i, test_name in enumerate(tests.keys()):
        prefix_lines = list(range(1, task_json.prefix.strip().count("\n")+2))
        wrap_get_test_result = lambda queue: get_test_result(tests[test_name], test_name, task_json.prefix+submission.code, prefix_lines, queue=queue)
        test_result = run_with_timeout(wrap_get_test_result, 5)
        if test_result is None:
            submission.type = "timed_out_submission"
            await db.database.log_code_submission(submission)
            raise asyncio.TimeoutError
        test_results.append(test_result)
        if test_results[i]["status"] == 0:
            valid_solution = False
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
        course = await db.database.get_course(unique_name=user.enrolled_courses[0])
        if course.curriculum == user.tasks_completed:
            if user.enrolled_courses[0] not in user.courses_completed:
                user.courses_completed.append(user.enrolled_courses[0]) #TODO: Unsafe, secure this
        await db.database.update_user(user)
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await db.database.log_code_submission(tested_submission)
    return  {"submission_id": str(tested_submission.id)}

@router.post("/mc_submit")
async def handle_mc_submission(submission: Code_submission, user: User = Depends(current_active_user)):
    user_id = user.id
    task_id = submission.task_unique_name
    task_json = await db.database.get_task(str(task_id))
    
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
        course = await db.database.get_course(unique_name=user.enrolled_courses[0])
        if course.curriculum == user.tasks_completed:
            if user.enrolled_courses[0] not in user.courses_completed:
                user.courses_completed.append(user.enrolled_courses[0]) #TODO: Unsafe, secure this
        await db.database.update_user(user)
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await db.database.log_code_submission(tested_submission)
    return  {"submission_id": str(tested_submission.id)}

def get_test_result(test_code, test_name, submission_code, prefix_lines, queue):
    run_test_code = """
try:
    {0}()
    test_result = 1
    test_message = ""
except AssertionError as e:
    test_result = 0
    test_message = str(e)
    print(e)""".format(test_name)
    test_submission_code = """
submission_captured_output = StringIO()
unsafe_sys_import.stdout = submission_captured_output
{0}
unsafe_sys_import.stdout = __stdout__
submission_captured_output = submission_captured_output.getvalue().strip()
{1}

{2}
    """.format(submission_code, test_code, run_test_code)
    #print(test_submission_code)
    #exec(test_submission_code, globals())
    global test_result
    global test_message
    try:
        
        save = check_user_code(submission_code, prefix_lines)
        if save:
            #exec(compile(parsed_ast, filename="<parsed_ast>", mode="exec"), globals())
            exec(test_submission_code, globals())
            result_message = "Test success" if test_result else "Test failure:"
        queue.put({"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()})
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}   
    except BaseException as e:
        test_result = 0
        result_message = "Error or Exception:"
        test_message = str(e)
        queue.put({"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()})
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
