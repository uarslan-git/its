import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from submissions import handle_submissions
from tasks import handle_tasks
from feedback import handle_feedback
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.include_router(handle_submissions.router)
app.include_router(handle_tasks.router)
app.include_router(handle_feedback.router)

# TODO: Hiermit in Hinblick auf security auseinandersetzen!
origins = ["*"]
#origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# Check connection status
@app.get("/status")
async def get_status():
    return {"message": "Connected!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
