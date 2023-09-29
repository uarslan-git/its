from submissions.schemas import Code_submission
from beanie import PydanticObjectId

class Run_code_submission(Code_submission):
    run_arguments: dict

    class Settings: 
        name = "Submission"

class Evaluated_run_code_submission(Code_submission):
    run_arguments: dict
    run_output: str
    user_id: PydanticObjectId

    class Settings: 
        name = "Submission"