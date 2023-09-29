from beanie import Document
from typing import Optional


class Task(Document):
    unique_name: str
    display_name: str
    task: str
    example_solution: str
    tests: dict
    type: str
    prefix: str
    arguments: list
    function_name: Optional[str]