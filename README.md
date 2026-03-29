# Telegram to Discord Relay

A simple relay that forwards messages from a Telegram channel to a Discord channel.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` file:
   - `TELEGRAM_API_ID` - Your Telegram API ID
   - `TELEGRAM_API_HASH` - Your Telegram API hash
   - `TELEGRAM_STRING_SESSION` - Your Telegram session string
   - `DISCORD_WEBHOOK_URL` - Your Discord webhook URL
   - `TG_CHANNEL` - The Telegram channel to monitor

3. Run the relay:
   ```
   python main.py
   ```

## Features

- Forwards text messages from Telegram to Discord
- Handles images and documents as attachments
- Preserves message formatting and metadata