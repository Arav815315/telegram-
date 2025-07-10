from telethon import TelegramClient, events
from io import BytesIO
import os

api_id = int(os.environ["api_id"])
api_hash = os.environ["api_hash"]
SOURCE_CHANNEL = int(os.environ["source_channel"])
DEST_CHANNEL = int(os.environ["dest_channel"])

client = TelegramClient("anon", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    print("📥 New message received!")
    msg = event.message

    if msg.video:
        print("🎥 Video detected, downloading...")
        bio = BytesIO()
        bio.name = "video.mp4"
        await client.download_media(msg, file=bio)
        bio.seek(0)
        await client.send_file(DEST_CHANNEL, file=bio, caption=msg.text or "")
        print("✅ Video forwarded!")
    else:
        print("❌ Not a video. Skipping.")

print("🚀 Bot is starting...")
client.start()
client.run_until_disconnected()
