from pydantic import BaseModel
from beanie import PydanticObjectId
from beanie import Document


# class Code_submission(BaseModel):
class Code_submission(Document):
    task_unique_name: str
    code: str
    log: str
    submission_time: dict
    type: str

    class Settings:
        name = "Submission"
        is_root=True

class Tested_code_submission(Code_submission):
    valid_solution: bool
    test_results: list
    user_id: PydanticObjectId

    class Settings: 
        name = "Submission"
