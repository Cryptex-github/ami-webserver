from fastapi import Request, Response
from fastapi.responses import ORJSONResponse
import os

TOKEN = os.getenv("AUTH")

async def auth(request, call_next):
    if request.url.path in ["/", "/robots.txt"]:
        return await call_next(request)
    
    try:
        token = request.headers["Authorization"]
        if not token:
            return ORJSONResponse({"message": "Missing authorization header"}, status_code=401)
        
        if token == TOKEN:
            return await call_next(request)
        
        return ORJSONResponse({"message": "Invalid token"}, status_code=401)
    
    except KeyError:
        return ORJSONResponse({"message": "Missing authorization header"}, status_code=401)
