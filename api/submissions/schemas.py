from pydantic import BaseModel
from beanie import PydanticObjectId
from beanie import Document
from typing import Optional

# class Code_submission(BaseModel):
class Code_submission(Document):
    task_unique_name: str
    course_unique_name: str
    code: str
    submission_time: dict
    type: str
    selected_choices: Optional[list]

    class Settings:
        name = "Submission"
        is_root=True

class Tested_code_submission(Code_submission):
    valid_solution: bool
    test_results: list
    user_id: PydanticObjectId
    possible_choices: Optional[list]
    correct_choices: Optional[list]

    class Settings: 
        name = "Submission"
