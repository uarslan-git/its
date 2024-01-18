"""General Settings class for the app. In later iterations, I see no need to have such general settings and most settings should probably be set on course level.
"""
from pydantic import BaseModel
from beanie import PydanticObjectId
from beanie import Document
from typing import Optional

class Settings(Document):
    ollama_url: str
