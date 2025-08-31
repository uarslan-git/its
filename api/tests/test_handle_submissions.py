import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_incorrect_code_submit(authenticated_client: AsyncClient):
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": "def factorial(n): return 1",
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Test failure"), f"Incorrect message prefix: {message} instead of Test failure"


@pytest.mark.asyncio
async def test_correct_code_submit(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 1, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Test success"), f"Incorrect message prefix: {message} instead of Test success"


@pytest.mark.asyncio
async def test_syntax_error_handling(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception"), f"Incorrect message prefix: {message} instead of Error or Exception"


@pytest.mark.asyncio
async def test_import_statement_refusal(authenticated_client: AsyncClient):
    code = '''
import os
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: Imports are not allowed in this context"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_from_import_statement_refusal(authenticated_client: AsyncClient):
    code = '''
from os import system
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: Imports are not allowed in this context"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_delete_refusal(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    return(n)
del test_result
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: Deletes are not allowed in this context"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_global_refusal(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    return(n)
global test_result
test_result = 1
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: Global Scope is not allowed"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_nonlocal_refusal(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    test_result = 0
    def change_result():
        nonlocal test_result
        test_result = 1
    change_result()
    return(n)
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: Nonlocal Scope is not allowed"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_exec_refusal(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    return(n)
exec("import os")
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: exec() is not allowed in this context"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_eval_refusal(authenticated_client: AsyncClient):
    code = '''
def factorial(n):
    return(n)
eval("import os")
'''
    response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": 1,
                                                                     "code": code,
                                                                     "log": "True",
                                                                     "submission_id": "test",
                                                                     "submission_time": ""}),
                                                                     )
    payload = response.json()
    assert payload['test_results'][0]['status'] == 0, "Incorrect status code"
    message = payload['test_results'][0]['message']
    assert message.startswith("Error or Exception: eval() is not allowed in this context"), f"Incorrect message prefix: {message}"


@pytest.mark.asyncio
async def test_intersecting_skills_update(monkeypatch, authenticated_client: AsyncClient):
    """
    Test that the intersecting skills integration works.
    This test mocks the judge0 call and the database calls.
    """
    # Mock the PFA model
    with patch("models.domain.submissions.submissions.PFA_Model") as mock_pfa_model:
        # Mock the execute_code_judge0 function
        with patch("models.domain.submissions.submissions.execute_code_judge0", new_callable=AsyncMock) as mock_execute_code_judge0:
            # Set the return value of the mock
            mock_execute_code_judge0.return_value = '##!serialization!##{"test_result": 1, "test_message": "Test success"}##!serialization!##'

            # Mock the database calls
            with patch("db.database.get_task") as mock_get_task, \
                 patch("db.database.get_course_enrollment") as mock_get_course_enrollment, \
                 patch("db.database.update_course_enrollment") as mock_update_course_enrollment, \
                 patch("db.database.log_code_submission") as mock_log_code_submission, \
                 patch("db.database.get_course") as mock_get_course, \
                 patch("db.database.get_courses_by_skills") as mock_get_courses_by_skills:

                # Set the return values of the mocks
                mock_get_task.return_value = AsyncMock(type="Function", tests={"test": "test"}, prefix="")
                mock_get_course_enrollment.return_value = AsyncMock(tasks_completed=[], completed=False)
                mock_get_course.return_value = AsyncMock(competencies=["Competency1"], curriculum=["greet"])
                mock_get_courses_by_skills.return_value = AsyncMock()

                # Call the submit endpoint
                response = await authenticated_client.post("/api/submit", content=json.dumps({"task_unique_name": "greet",
                                                                             "course_unique_name": "Intro_to_Py",
                                                                             "code": "print('hello')",
                                                                             "log": "True",
                                                                             "submission_id": "test",
                                                                             "submission_time": ""}),
                                                                             )

                # Assert that the response is successful
                assert response.status_code == 200

                # Assert that the PFA model was updated
                mock_pfa_model.return_value.update_course_weights.assert_called_once()
