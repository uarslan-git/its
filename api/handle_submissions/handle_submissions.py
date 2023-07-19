from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# run test on submission
class Code_submission(BaseModel):
    code: str

# task schema
class task(BaseModel):
    task_markdown: str
    example_solution: str
    tests: list

@router.post("/code_submit")
async def get_test_result(submission: Code_submission):
# TODO: Funktion: (test_eingabe, soll_ausgabe) -> test_feedback
    test_code = """
{0}
        

def test_factorial(factorial):
    # Test factorial of 0
    assert factorial(0) == 1
    
    # Test factorial of positive numbers
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800

result = 0
try:     
    test_factorial(factorial)
    print("should work")
    result = 1
except AssertionError as e:
    result = 0
    print(e)

    """.format(submission.code)
    print(test_code)
    exec(test_code, globals())
    result_status = "succsess!" if result else "failure"
    print(result_status)
    print(result)
    return  {"test_result": result_status}