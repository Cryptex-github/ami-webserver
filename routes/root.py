from fastapi import APIRouter
from fastapi.responses import FileResponse
from werkzeug import safe_join

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
    file_path = safe_join("/app/uploads/", filename)
    return FileResponse(path=file_path, filename=filename)
