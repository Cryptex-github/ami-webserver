from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import FileResponse
from werkzeug import safe_join

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/uploads/{filename}")
async def uploads(filename: str):
    file_path = safe_join("/app/uploads/", filename)
    return FileResponse(path=file_path, filename=filename)