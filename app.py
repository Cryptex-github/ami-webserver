from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from auth.auth import auth
from routes.api import api_router
from routes.root import root_router


app = FastAPI()
app.include_router(api_router, prefix="/api")
app.add_middleware(BaseHTTPMiddleware, auth)
app.add_middleware(HTTPSRedirectMiddleware)

