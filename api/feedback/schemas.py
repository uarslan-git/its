from submissions.schemas import Code_submission, Tested_code_submission
from beanie import Document

class Feedback_submission(Code_submission):

    class Settings: 
        name = "Submission"

class Evaluated_feedback_submission(Feedback_submission, Tested_code_submission):
    
    feedback_method: str
    feedback: str

    class Settings: 
        name = "Submission"

class Url(Document):
    
    url: str