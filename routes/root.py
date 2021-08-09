import os

UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
from fastapi import APIRouter
from fastapi.responses import FileResponse
from werkzeug.utils import safe_join

root_router = APIRouter()


@root_router.get("/")
async def root():
    return {"Hello": "World"}

@root_router.get("/robots.txt")
async def robots():
    return """
User-agent: *
Disallow:
"""

@root_router.get("/uploads/{filename}")
async def uploads(filename: str):
    file_path = safe_join(UPLOAD_PATH, filename)
    return FileResponse(path=file_path, filename=filename)
