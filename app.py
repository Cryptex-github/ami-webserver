from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import FileResponse
from auth.auth import auth
from routes.api import api_router
from werkzeug import safe_join

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.add_middleware(BaseHTTPMiddleware, auth)
app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/uploads/{filename}")
async def uploads(filename: str):
    file_path = safe_join("/app/uploads/", filename)
    return FileResponse(path=file_path, filename=filename)