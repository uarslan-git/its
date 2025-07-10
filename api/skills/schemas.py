from beanie import Document
from typing import Optional, Union
from enum import StrEnum


class Skill(Document):
    name: str
    value: int
    gain: int