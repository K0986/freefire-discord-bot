# Free Fire Like Discord Bot

A Discord bot that sends likes to Free Fire profiles using the Free Fire Like API.

## Features
- Send likes to Free Fire profiles using the `!like` command
- Get player information and like counts
- Easy to use command interface

## Setup and Deployment on Heroku

1. Create a Discord Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" tab and create a bot
   - Copy the bot token
   - Under "OAuth2" > "URL Generator", select "bot" scope and "Send Messages" permission
   - Use the generated URL to invite the bot to your server

2. Deploy to Heroku:
   - Fork or clone this repository
   - Create a new Heroku app
   - Connect your GitHub repository to Heroku
   - Add the following Config Var in Heroku Settings:
     - Key: `DISCORD_BOT_TOKEN`
     - Value: Your Discord bot token
   - Deploy the app and ensure it's running as a worker dyno

## Usage

Once the bot is running and invited to your server, you can use the following command:

```
!like <uid>
```

Replace `<uid>` with the Free Fire player's UID you want to send likes to.

Example:
```
!like 123456789
```

The bot will respond with the player's information and the number of likes sent.
