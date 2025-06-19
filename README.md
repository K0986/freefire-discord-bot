# Free Fire Like Discord Bot

A Discord bot that sends likes to Free Fire profiles using the Free Fire Like API.

## Features
- Send likes to Free Fire profiles using the `!like` command
- Beautiful embed messages with like count information and thumbnail images
- Error handling and logging
- Easy deployment on Railway

## Deployment on Railway

1. **Prerequisites**:
   - Create a Discord bot at [Discord Developer Portal](https://discord.com/developers/applications)
   - Get your bot token
   - Add bot to your server with required permissions (Send Messages, Embed Links, Read Message History)

2. **Deploy on Railway**:
   - Fork this repository
   - Go to [Railway](https://railway.app/)
   - Create a new project
   - Choose "Deploy from GitHub repo"
   - Select your forked repository
   - Add Environment Variable:
     - Key: `DISCORD_BOT_TOKEN`
     - Value: Your Discord bot token
   - Deploy!

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export DISCORD_BOT_TOKEN=your_token_here

# Run the bot
python discord_bot.py
```

## Usage
Once the bot is running, use the following command in your Discord server:
```
!like <uid>
```
Replace `<uid>` with the Free Fire player's UID you want to send likes to.

## Features
- Embedded messages for better presentation with thumbnail images
- Error handling and logging
- Automatic reconnection on failure
- Status updates for each request
- **Important:** Ensure the bot has the necessary permissions in your server: Send Messages, Embed Links, and Read Message History.
