from telethon import TelegramClient
from io import BytesIO
import asyncio
import os

api_id = int(os.environ["api_id"])
api_hash = os.environ["api_hash"]
SOURCE_CHANNEL = int(os.environ["source_channel"])
DEST_CHANNEL = int(os.environ["dest_channel"])

client = TelegramClient("anon", api_id, api_hash)  # use the same session name

async def main():
    async for msg in client.iter_messages(SOURCE_CHANNEL, limit=5):
        if msg.video:
            bio = BytesIO()
            bio.name = "video.mp4"
            await client.download_media(msg, file=bio)
            bio.seek(0)
            await client.send_file(DEST_CHANNEL, file=bio, caption=msg.text or "")

with client:
    client.loop.run_until_complete(main())
