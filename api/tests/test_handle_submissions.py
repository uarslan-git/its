from fastapi.testclient import TestClient
import json
from submissions.handle_submissions import router
import pytest
#When using pytest:

client = TestClient(router)

@pytest.mark.asyncio
async def test_incorrect_code_submit():
    response = client.post("/code_submit", content=json.dumps({"task_id": 1, "code": "def factorial(n):\n    return(1)", "log": "True"}))
    payload = response.json()
    print(payload)
    assert payload['test_results'][0]['status'] == 0, "False positive test"
    assert payload['test_results'][0]['message'] == "failure", "Incorrect message"

#TODO: Check why multiple async tests are not working!
@pytest.mark.asyncio
async def test_correct_code_submit():
    response = client.post("/code_submit", content=json.dumps({"task_id": 1, 
                                                               "code": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
                                                               "log": "False"}))
    payload = response.json()
    print(payload)
    assert payload['test_results'][0]['status'] == 1, "False negative test"
    assert payload['test_results'][0]['message'] == "success", "Incorrect message"


def test_import_statement_refusal():
    response = client.post("/code_submit", content=json.dumps({"task_id": 1, 
                                                               "code": "import os\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
                                                               "log": "False"}))
    payload = response.json()
    assert payload['test_results'][0]['message'] == "Imports are not allowed in this context.", "Potentially malicious imports are not detected"

def test_from_import_statement_refusal():
    response = client.post("/code_submit", content=json.dumps({"task_id": 1, 
                                                               "code": "from os import system\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
                                                               "log": "False"}))
    payload = response.json()
    assert payload['test_results'][0]['message'] == "Imports are not allowed in this context.", "Potentially malicious imports are not detected"


if __name__ == "__main__":
    event_loop.run_until_complete(print(test_incorrect_code_submit()))
    print(test_correct_code_submit())
    print(test_import_statement_refusal())
    print(test_from_import_statement_refusal())