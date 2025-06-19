import discord
from discord.ext import commands
import os
import logging
import aiohttp

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_bot')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# API configuration
API_URL = "https://freefire-like-nine.vercel.app"

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name="like", help="Send a like to a Free Fire UID")
async def like(ctx, uid: str):
    try:
        await ctx.send(f"Sending like to UID: {uid}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}?uid={uid}", timeout=10) as response:
                if response.status != 200:
                    await ctx.send(f"Failed to send like. API returned status {response.status}.")
                    return
                data = await response.json()
                if data.get("status") == 1:
                    await ctx.send(f"👍 Like sent successfully to player {data.get('player', 'Unknown')}! Likes before: {data.get('likes_before')}, Likes after: {data.get('likes_after')}.")
                elif data.get("status") == 2:
                    await ctx.send(f"ℹ️ No new likes added. Player {data.get('player', 'Unknown')} already has {data.get('likes_after')} likes.")
                else:
                    await ctx.send(f"⚠️ Could not send like. Message: {data.get('message', 'Unknown error')}")
    except Exception as e:
        logger.error(f"Error in like command: {str(e)}")
        await ctx.send("❌ An error occurred while processing your request. Please try again later.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("No Discord bot token found!")
        raise ValueError("DISCORD_BOT_TOKEN environment variable is required")
    bot.run(token)
