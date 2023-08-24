from _ast import Call, Del, Delete, Global, Interactive, Load, Nonlocal, Store
from typing import Any
from fastapi import APIRouter, Depends
# from fastapi.encoders import jsonable_encoder

from os import path
import ast
from users.handle_users import current_active_user

from db.db_connector_beanie import User
from submissions.schemas import Code_submission, Tested_code_submission
from tasks.schemas import Task

# import motor.motor_asyncio
import db

router = APIRouter()


# run test on submission
#class Code_submission(BaseModel):
#    task_id: str
#    code: str
#    log: str
#    submission_id: str
#    submission_time: str

#class Tested_code_submission(Code_submission):
#    test_results: list
#    user_id: PydanticObjectId


# task schema
""" class task(BaseModel):
    task_id: int
    task_markdown: str
    example_solution: str
    tests: list """

@router.post("/code_submit")
async def handle_code_submission(submission: Code_submission, user: User = Depends(current_active_user)):
# TODO: Funktion: (test_eingabe, soll_ausgabe) -> test_feedback
    user_id = user.id
    task_id = submission.task_id
    task_json = await db.database.get_task(str(task_id))
    tests = task_json['tests']
    test_results = []
    for test_name in tests.keys():
        test_results.append(get_test_result(test_code=tests[test_name], test_name=test_name, submission_code=submission.code))
    # Log code submit to database
    tested_submission = Tested_code_submission(log = submission.log, task_id = submission.task_id, 
                                               code = submission.code, test_results= test_results,
                                               submission_id=submission.submission_id, user_id=user_id,
                                               submission_time=submission.submission_time)
    #TODO: Check whether this whole log-loic is necassary. User opt-out only for interaction-logging?
    if (submission.log == "True"):
        await db.database.log_code_submission(tested_submission)
    return  {"test_results": test_results}


def get_test_result(test_code, test_name, submission_code):
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
{0}

{1}

{2}
    """.format(submission_code, test_code, run_test_code)
    #print(test_submission_code)
    #exec(test_submission_code, globals())
    global test_result
    global test_message
    try:
        parsed_ast = ast.parse(submission_code)
        save = check_submission_code(ast_tree=parsed_ast)
        if save:
            #exec(compile(parsed_ast, filename="<parsed_ast>", mode="exec"), globals())
            exec(test_submission_code, globals())
            result_message = "Test success" if test_result else "Test failure:"
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}
    except BaseException as e:
        test_result = 0
        result_message = "Error or Exception:"
        test_message = str(e)
        return {"test_name": test_name, "status": test_result, "message": "{0} {1}".format(result_message, test_message).strip()}


def check_submission_code(ast_tree):
    class ImportVisitor(ast.NodeVisitor):
        def __init__(self):
            self.found_imports = False

        def visit_Import(self, node):
            self.found_imports = True # TODO: Can the bool be removed?
            raise Exception("Imports are not allowed in this context.")

        def visit_ImportFrom(self, node):
            self.found_imports = True
            raise Exception("Imports are not allowed in this context")
        
        def visit_Interactive(self, node: Interactive):
            raise Exception("Interactive Mode is not allowed")
        
        def visit_Delete(self, node: Delete):
            raise Exception("Deletes are not allowed in this context")
        
        def visit_Global(self, node: Global):
            raise Exception("Global Scope is not allowed")

        def visit_Nonlocal(self, node: Nonlocal):
            raise Exception("Nonlocal Scope is not allowed")
        
        #def visit_Load(self, node: Load) -> Any:
        #    raise Exception("Load not allowed")
        
        #def visit_Store(self, node: Store) -> Any:
        #    raise Exception("Store not allowed")
        
        def visit_Del(self, node: Del) -> Any:
            raise Exception("Del not allowed")
        
        def visit_Call(self, node: Call) -> Any:
            if node.func.id == "exec":
                raise Exception("exec() is not allowed in this context")
            if node.func.id in ["eval", "open", "breakpoint", "callable",
                                 "delattr", "dir", "getattr", "globals",
                                 "hasattr", "help", "id", "input", "locals", 
                                 "memoryview", "property", "setattr", 
                                 "staticmethod", "vars", "__import__"]:
                fun_id = node.func.id
                raise Exception(f"{fun_id}() is not allowed in this context")
            self.generic_visit(node)


    visitor = ImportVisitor()
    visitor.visit(ast_tree)
    return not visitor.found_imports
