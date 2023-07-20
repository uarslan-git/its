from fastapi.testclient import TestClient
import json
from handle_submissions import router
#When using pytest:
#.from handle_submissions import router
client = TestClient(router)

def test_code_submit():
    response = client.post("/code_submit", content=json.dumps({"task_id": 1, "code": "def factorial(n):\n    return(1)"}))
    print(response)

if __name__ == "__main__":
    test_code_submit()

