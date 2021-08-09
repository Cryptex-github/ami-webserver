import os

from dotenv import dotenv
from fastapi import APIRouter, UploadFile

dotenv()
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOKS')
SECRET_KEY = os.getenv('SECRET_KEY')
import hmac
import secrets
from datetime import datetime
from mimetypes import guess_extension

import aiohttp
import discord
from fastapi.response import Response, ORJSONResponse
webhook = discord.Webhook.from_url(DISCORD_WEBHOOK, adapter=discord.AsyncWebhookAdapter(aiohttp.ClientSession()))

api_router = APIRouter()

@api_router.post("/upload")
async def upload(file: UploadFile):
    filename = secrets.token_urlsafe(12)
    ext = guess_extension(file.content_type)
    if ext is None:
        return Response(content="Unsupported file type", status_code=415)
    ext = ext.replace(".", "")
    filename = f"{filename}.{ext}"
    if os.path.isdir("/app/uploads/") is False:
        os.mkdir("/app/uploads/")
    
    save_path = safe_join("/app/uploads/", filename)
    await file.seek(0)

    await file.save(save_path)

    url = f"https://amidiscord.xyz/uploads/{filename}"

    hmac_hash = hmac.new(SECRET_KEY.encode(), filename.encode(), "sha256").hexdigest()

    delete_url = f"https://amidiscord.xyz/api/delete-file/{hmac_hash}/{filename}"

    embed = discord.Embed(title="**New file has been uploaded!**", description=url, timestamp=datetime.utcnow(), color=discord.Color.random())
    embed.add_field(name="URL", value=url)
    embed.add_field(name="Deletion URL", value=delete_url)
    embed.set_image(url=url)

    await webhook.send(embed=embed)

    return ORJSONResponse({"url": url, "delete_url": delete_url}, status_code=201)

@api_router.delete("/delete-file/{hmac_hash}/{filename}")
async def delete_file(hmac_hash: str, filename: str):
    _hmac_hash = hmac.new(SECRET_KEY.encode(), f"{filename}.{filename.split('.')[-1]}".encode(), "sha256").hexdigest()
    if hmac.compare_digest(hmac_hash, _hmac_hash) is False:
        return Response(content="File not found", status_code=404)
    file_path = safe_join("/app/uploads/", filename)
    if os.path.isfile(file_path) is False:
        return Response(content="File not found", status_code=404)
    os.remove(file_path)
    return Response(content="File deleted", status_code=204)

    
    