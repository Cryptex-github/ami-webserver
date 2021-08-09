import os
from aiofile import async_open

UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from werkzeug.utils import safe_join

root_router = APIRouter()

@root_router.get("/", response_class=HTMLResponse)
async def root():
    async with async_open(os.path.join(os.getcwd(), "templates", "index.html"), "r") as afp:
        return await afp.read()

@root_router.get("/robots.txt")
async def robots():
    return PlainTextResponse("""
User-agent: *
Disallow:
""", media_type="text/plain")
