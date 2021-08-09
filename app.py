from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from auth.auth import auth
from routes.api import api_router
from routes.root import root_router

origins = [
    "http://amidiscord.xyz",
    "https://amidiscord.xyz",
    "http://localhost:80",
]

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(api_router, prefix="/api")
app.include_router(root_router, prefix="/")
app.add_middleware(BaseHTTPMiddleware, auth)
app.add_middleware(CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)

