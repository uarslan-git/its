from _ast import Call, Del, Delete, Global, Interactive, Nonlocal, Name
from typing import Any
from fastapi import APIRouter, Depends
import asyncio
from os import path
import ast
from users.handle_users import current_active_verified_user
from db.db_connector_beanie import User
from submissions.schemas import Code_submission, Tested_code_submission
from tasks.schemas import Task
from models.domain.submissions import handle_submission
from config import config

from db import database
from sys import __stdout__
import aiohttp
import json

router = APIRouter()

@router.post("/submit")
async def submit(submission: Code_submission, user: User = Depends(current_active_verified_user)):
    try:
        return await handle_submission(submission, user)
    except Exception as e:
        test_result = 0
        exception_type = type(e)
        test_message = str(e)
        # "test_name": test_name
        return {"status": test_result, "message": f"{exception_type}: {test_message}".strip()}
    
@router.get("/submission/feedback/{submission_id}")
async def send_feedback(submission_id):
    feedback = await database.get_submission(str(submission_id))
    return feedback
