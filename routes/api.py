import os

from fastapi import APIRouter, UploadFile, Form
from aiofile import async_open

UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
SECRET_KEY = os.getenv('SECRET_KEY')
import hmac
import secrets
from datetime import datetime
from magic import from_buffer
from mimetypes import guess_extension

import aiohttp
import discord
from fastapi.responses import Response, ORJSONResponse
from werkzeug.utils import safe_join
webhook = discord.Webhook.from_url(DISCORD_WEBHOOK, adapter=discord.AsyncWebhookAdapter(aiohttp.ClientSession()))

api_router = APIRouter()

@api_router.post("/upload")
async def upload(file: UploadFile = Form(...)):
    filename = secrets.token_urlsafe(12)
    file_bytes = await file.read(8000)
    mine = from_buffer(file_bytes, mime=True).lower()
    ext = guess_extension(mine)
    if ext is None:
        return Response(content="Unsupported file type", status_code=415)
    ext = ext.replace(".", "")
    filename = f"{filename}.{ext}"
    if os.path.isdir(UPLOAD_PATH) is False:
        os.mkdir(UPLOAD_PATH)
    
    save_path = safe_join(UPLOAD_PATH, filename)
    await file.seek(0)
    
    async with async_open(save_path, "wb+") as afp:
        await afp.write(await file.read())
        afp.seek(0)

    url = f"https://cdn.amidiscord.xyz/uploads/{filename}"

    hmac_hash = hmac.new(SECRET_KEY.encode(), filename.encode(), "sha256").hexdigest()

    delete_url = f"https://cdn.amidiscord.xyz/api/delete-file/{hmac_hash}/{filename}"

    embed = discord.Embed(title="**New file has been uploaded!**", description=url, timestamp=datetime.utcnow(), color=discord.Color.random())
    embed.add_field(name="URL", value=f"[**Click here to view!**]({url})")
    embed.add_field(name="Deletion URL", value=f"[**Click here to delete!**]({delete_url})")
    embed.set_image(url=url)

    await webhook.send(embed=embed)

    return ORJSONResponse({"url": url, "delete_url": delete_url}, status_code=201)

@api_router.get("/delete-file/{hmac_hash}/{filename}")
async def delete_file(hmac_hash: str, filename: str):
    _hmac_hash = hmac.new(SECRET_KEY.encode(), f"{filename}.{filename.split('.')[-1]}".encode(), "sha256").hexdigest()
    if hmac.compare_digest(hmac_hash, _hmac_hash) is False:
        return Response(content="File not found", status_code=404)
    file_path = safe_join(UPLOAD_PATH, filename)
    if os.path.isfile(file_path) is False:
        return Response(content="File not found", status_code=404)
    os.remove(file_path)
    return Response(content="File deleted", status_code=204)

    
    
