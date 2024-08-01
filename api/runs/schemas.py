from submissions.schemas import Base_Submission
from beanie import PydanticObjectId

class Run_code_submission(Base_Submission):
    run_arguments: dict

    class Settings: 
        name = "Submission"

class Evaluated_run_code_submission(Base_Submission):
    run_arguments: dict
    run_output: str
    user_id: PydanticObjectId

    class Settings: 
        name = "Submission"