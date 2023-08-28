from pydantic import BaseModel
from beanie import PydanticObjectId
from beanie import Document


# class Code_submission(BaseModel):
class Code_submission(Document):
    task_unique_name: str
    code: str
    log: str
    submission_id: str
    submission_time: str

    class Settings:
        name = "Submission"

class Tested_code_submission(Code_submission):
    valid_solution: bool
    test_results: list
    user_id: PydanticObjectId

    class Settings: 
        name = "Submission"
