import os
import logging

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from discord_webhook import DiscordWebhook, DiscordEmbed

# Load environment variables from .env file
from dotenv import load_dotenv
import asyncio
load_dotenv()

# Get environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
string_session = os.getenv('TELEGRAM_STRING_SESSION')
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
tg_channels = os.getenv('TG_CHANNELS').split(',')

logging.basicConfig(level=logging.INFO)

async def handle_new_message(event):
    """Handle new messages from Telegram channel"""
    try:
        message = event.message
        
        if not message:
            return
            
        # Create Discord embed
        embed = DiscordEmbed()
        
        # Set author
        sender = message.sender
        if sender:
            embed.set_author(name=sender.username or sender.first_name)
        
        # Set content
        text = ''
        if message.text:
            text = message.text
        
        # Handle images and other media
        media = message.media
        if media:
            if hasattr(media, 'photo'):
                text += f"\n[Photo]"
            elif hasattr(media, 'document'):
                text += f"\n[Document: {media.document.attributes[0].file_name}]"
            elif hasattr(media, 'webpage'):
                text += f"\n[Webpage: {media.webpage.url}]"
            
        embed.description = text
        
        # Set timestamp
        embed.set_timestamp()
        
        embed.add_embed_field(name="Source", value=event.chat.title)
        embed.add_embed_field(name="username", value=sender.username or sender.first_name)
        
        # Send to Discord
        webhook = DiscordWebhook(url=discord_webhook_url, embeds=[embed])
        
        # Handle attachments
        if message.photo:
            photo = message.photo
            filename = f"photo_{photo.date.timestamp()}.jpg"
            await client.download_media(message.photo, filename)
            with open(filename, "rb") as f:
                webhook.add_file(file=f.read(), filename=filename)
        
        if message.document:
            document = message.document
            filename = document.attributes[0].file_name
            await client.download_media(message.document, filename)
            with open(filename, "rb") as f:
                webhook.add_file(file=f.read(), filename=filename)
        
        response = webhook.execute()
        if response:
            logging.info(f"Message forwarded to Discord: {text[:50]}...")
        else:
            logging.error("Failed to forward message to Discord")
            
    except Exception as e:
        logging.error(f"Error handling message: {e}")

async def main():
    """Main function to start the relay"""
    global client
    client = TelegramClient(StringSession(string_session), api_id, api_hash)
    
    await client.start()
    
    try:
        await client.get_dialogs()
        logging.info("Client connected successfully")
        
        # Get channel entities
        for channel in [await client.get_entity(c) for c in tg_channels]:
            logging.info(f"Monitoring Telegram channel: {channel.title}")
            
            client.add_event_handler(
                handle_new_message,
                events.NewMessage(forwards=False, chats=channel)
            )
        
        logging.info("Starting message relay service...")
        await client.run_until_disconnected() 
            
    except Exception as e:
        logging.error(f"Failed to start client: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())