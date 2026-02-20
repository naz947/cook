import asyncio
from telethon import TelegramClient
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

api_id_str = os.environ.get("TELEGRAM_API_ID", "").strip()
api_hash = os.environ.get("TELEGRAM_API_HASH", "").strip()
group_id_str = os.environ.get("GROUP_ID", "").strip()
topic_id = 5  # Change this to your topic ID

# Validate and convert
if not api_id_str or not api_hash or not group_id_str:
    raise ValueError(
        "Missing required environment variables:\n"
        f"  TELEGRAM_API_ID: {'❌' if not api_id_str else '✅'}\n"
        f"  TELEGRAM_API_HASH: {'❌' if not api_hash else '✅'}\n"
        f"  GROUP_ID: {'❌' if not group_id_str else '✅'}\n"
        "Please set these in GitHub Secrets or .env file"
    )

try:
    api_id = int(api_id_str)
    group_id = int(group_id_str)
except ValueError as e:
    raise ValueError(f"TELEGRAM_API_ID and GROUP_ID must be valid integers: {e}")

# Extract URLs from text
url_pattern = re.compile(r"https?://\S+")

async def main():
    
    async with TelegramClient("session", api_id, api_hash) as client:
        print("Connecting to Telegram...")
        data = []
        
        try:
            async for msg in client.iter_messages(
                group_id,
                reply_to=topic_id,
                limit=None
            ):
                if not msg.text:
                    continue
                
                urls = url_pattern.findall(msg.text)
                
                data.append({
                    "id": msg.id,
                    "text": msg.text,
                    "urls": urls,
                    "date": str(msg.date)
                })
            
            # Reverse to get oldest → newest order
            data.reverse()
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(data)} messages to data.json")
            
        except Exception as e:
            print(f"❌ Error fetching messages: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(main())