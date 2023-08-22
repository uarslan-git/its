import uvicorn
from fastapi import FastAPI, Depends
from fastapi import APIRouter
from submissions import handle_submissions
from tasks import handle_tasks
from feedback import handle_feedback
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from users import handle_users
from users import schemas as user_schemas
from beanie import init_beanie
from db import database_beanie, User

app = FastAPI()
app.include_router(handle_submissions.router)
app.include_router(handle_tasks.router)
app.include_router(handle_feedback.router)

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

@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=database_beanie,
        document_models=[
            User,
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
