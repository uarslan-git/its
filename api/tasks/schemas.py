from beanie import Document


class Task(Document):
    unique_name: str
    display_name: str
    task: str
    example_solution: str
    tests: dict