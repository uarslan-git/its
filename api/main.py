import uvicorn
from fastapi import FastAPI, Depends
from fastapi import APIRouter
from submissions import handle_submissions
from attempts import handle_attempts
from submissions.schemas import Code_submission, Tested_code_submission
from tasks import handle_tasks
from feedback import handle_feedback
from courses import handle_courses
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from users import handle_users
from users import schemas as user_schemas
from courses.schemas import Course
from tasks.schemas import Task
from attempts.schemas import Attempt, AttemptState
from beanie import init_beanie
from db import db_connector_beanie
from users.schemas import User

app = FastAPI()
app.include_router(handle_submissions.router)
app.include_router(handle_tasks.router)
app.include_router(handle_feedback.router)
app.include_router(handle_attempts.router)
app.include_router(handle_courses.router)

# User Router and database setup
app.include_router(
    handle_users.fastapi_users.get_auth_router(handle_users.auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    handle_users.fastapi_users.get_register_router(user_schemas.UserRead, user_schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    handle_users.fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    handle_users.fastapi_users.get_verify_router(user_schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    handle_users.fastapi_users.get_users_router(user_schemas.UserRead, user_schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(handle_users.current_active_user)):
    return {"message": f"Hello {user.email}!"}

db_connection_beanie = db_connector_beanie.database()

@app.on_event("startup")
async def on_startup():

    await init_beanie(
        database=db_connection_beanie.db,
        document_models=[
            User, Code_submission, Tested_code_submission, Course, Task, Attempt, AttemptState
        ],
    )

# TODO: Hiermit in Hinblick auf security auseinandersetzen!
#origins = ["*"]
origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Check connection status
@app.get("/status")
async def get_status():
    return {"message": "Connected!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
