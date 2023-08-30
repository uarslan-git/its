from beanie import Document
from beanie import PydanticObjectId

class Attempt(Document):
    user_id: str
    task_unique_name: str
    state_log: list

class AttemptState(Document):
    attempt_id: str
    state_datetime: str
    code: str
    submission_id: str