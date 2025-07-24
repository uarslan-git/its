from pydantic import BaseModel
from typing import List


class Skill(BaseModel):
    name: str
    value: float
    gain: float

class SkillOverview(BaseModel):
    skill_list: List[Skill]