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
API_URL = "https://freefire-like-nine.vercel.app/like"

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name="like", help="Send a like to a Free Fire UID")
async def like(ctx, uid: str):
    try:
        await ctx.send(f"ℙ𝕣𝕠𝕔𝕖𝕤𝕤𝕚𝕟𝕘 like to UID: {uid}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}?uid={uid}", timeout=10) as response:
                if response.status != 200:
                    await ctx.send(f"Failed to send like. API returned status {response.status}.")
                    return
                data = await response.json()

                status = data.get("status")
                nickname = data.get("player", "Unknown")
                before = data.get("likes_before", "?")
                after = data.get("likes_after", "?")
                added = data.get("likes_added", int(after) - int(before) if str(before).isdigit() and str(after).isdigit() else 0)
                region = data.get("server_used", "Unknown")
                uid_display = data.get("uid", uid)

                if status == 1:
                    msg = (
                        f"┌  ACCOUNT\n"
                        f"├─ NICKNAME: {nickname}\n"
                        f"├─ UID: {uid_display}\n"
                        f"└─ RESULT:\n"
                        f"    ├─ ADDED: +{added}\n"
                        f"    ├─ BEFORE: {before}\n"
                        f"    └─ AFTER: {after}\n"
                        f"REGION: {region}"
                    )
                    await ctx.send(f"```{msg}```")

                elif status == 2:
                    msg = (
                        f"┌  ACCOUNT\n"
                        f"├─ NICKNAME: {nickname}\n"
                        f"├─ UID: {uid_display}\n"
                        f"└─ RESULT:\n"
                        f"    ├─ ADDED: +0 (No new like)\n"
                        f"    ├─ TOTAL LIKES: {after}\n"
                        f"    └─ STATUS: Already liked\n"
                        f"REGION: {region}"
                    )
                    await ctx.send(f"```{msg}```")

                else:
                    msg = (
                        f"┌  ERROR\n"
                        f"├─ UID: {uid_display}\n"
                        f"└─ MESSAGE: {data.get('message', 'Unknown error')}"
                    )
                    await ctx.send(f"```{msg}```")

    except Exception as e:
        logger.error(f"Error in like command: {str(e)}")
        await ctx.send("❌ An error occurred while processing your request. Please try again later.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("No Discord bot token found!")
        raise ValueError("DISCORD_BOT_TOKEN environment variable is required")
    bot.run(token)
