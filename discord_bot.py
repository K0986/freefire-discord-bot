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

CYBERPUNK_COLOR = 0x00FFEF  # Neon cyan color for cyberpunk style
CYBER_FONT = "𝕱𝖗𝖊𝖊𝖋𝖎𝖗𝖊-𝖑𝖎𝖐𝖊-𝕭𝖔𝖙"

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name="like", help="Send a like to a Free Fire UID")
async def like(ctx, uid: str):
    try:
        request_url = f"{API_URL}?uid={uid}"
        logger.info(f"Sending request to API URL: {request_url}")
        await ctx.send(f"⚡ Sending like to UID: `{uid}`...")
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url, timeout=10) as response:
                if response.status != 200:
                    await ctx.send(f"❌ Failed to send like. API returned status {response.status}.")
                    return
                data = await response.json()
                if data.get("status") == 1:
                    embed = discord.Embed(
                        title=f"⚡ {CYBER_FONT} ⚡",
                        description=f"**Player:** `{data.get('player', 'Unknown')}`",
                        color=CYBERPUNK_COLOR
                    )
                    embed.add_field(name="Likes Before", value=f"`{data.get('likes_before')}`", inline=True)
                    embed.add_field(name="Likes After", value=f"`{data.get('likes_after')}`", inline=True)
                    embed.set_footer(text=f"Server Used: {data.get('server_used', 'Unknown')}")
                    embed.set_thumbnail(url="https://i.imgur.com/3ZQ3ZQZ.png")  # Cyberpunk style thumbnail
                    await ctx.send(embed=embed)
                elif data.get("status") == 2:
                    embed = discord.Embed(
                        title=f"⚡ {CYBER_FONT} ⚡",
                        description=f"ℹ️ Player `{data.get('player', 'Unknown')}` already has `{data.get('likes_after')}` likes.",
                        color=CYBERPUNK_COLOR
                    )
                    embed.set_footer(text=f"Server Used: {data.get('server_used', 'Unknown')}")
                    embed.set_thumbnail(url="https://i.imgur.com/3ZQ3ZQZ.png")
                    await ctx.send(embed=embed)
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
