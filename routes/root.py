import os

UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from werkzeug.utils import safe_join

root_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@root_router.get("/", response_class=HTMLResponse)
async def root(request: Request, id: str):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})

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
