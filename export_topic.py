import asyncio
from telethon import TelegramClient
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
group_id = int(os.environ.get("GROUP_ID", "0"))
topic_id = 5  # Change this to your topic ID

# Extract URLs from text
url_pattern = re.compile(r"https?://\S+")

async def main():
    if not api_id or not api_hash or not group_id:
        raise ValueError("Missing required environment variables: TELEGRAM_API_ID, TELEGRAM_API_HASH, GROUP_ID")
    
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