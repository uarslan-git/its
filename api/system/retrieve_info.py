from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/about")
def get_about():
    filepath = os.path.join(os.path.dirname(__file__), "about.md")
    print(filepath)
    with open(filepath) as f:
        about_markdown = f.read()
    return({"about_markdown": about_markdown})

@router.get("/data_collection")
def get_about():
    filepath = os.path.join(os.path.dirname(__file__), "data_collection.md")
    print(filepath)
    with open(filepath) as f:
        data_collection_markdown = f.read()
    return({"data_collection_markdown": data_collection_markdown})