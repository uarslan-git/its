import asyncio
import pytest_asyncio
from httpx import AsyncClient
from main import app
from db import database
from users.schemas import UserCreate
import datetime

@pytest_asyncio.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def authenticated_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a test user
        user_in = UserCreate(
            email="testuser@example.com",
            password="password",
            username="testuser",
            verification_email="testuser@example.com",
            current_course="Intro_to_Py",
            enrolled_courses=["Intro_to_Py"],
            register_datetime={"$date": "2024-01-01T00:00:00.000Z"},
            settings={}
        )
        await database.db["users"].insert_one(user_in.dict())

        # Log in to get the cookie
        response = await client.post("/api/auth/jwt/login", data={"username": "testuser@example.com", "password": "password"})
        cookie = response.cookies.get("fastapi-users-auth")

        # Create a new client with the cookie
        client.cookies.set("fastapi-users-auth", cookie)
        yield client