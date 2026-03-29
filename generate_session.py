from telethon import TelegramClient
from telethon.sessions import StringSession
import sys

# Get API ID and API hash from command line arguments
api_id = int(sys.argv[1])
api_hash = sys.argv[2]

# Create a new client
client = TelegramClient(StringSession(), api_id, api_hash)

async def main():
    # Connect to Telegram
    await client.start()
    
    # Get the session string
    session_string = client.session.save()
    print(f"Your session string: {session_string}")
    
    # Disconnect
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())