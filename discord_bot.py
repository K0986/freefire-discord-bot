import discord
from discord.ext import commands
import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_bot')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# API configuration
API_URL = "https://freefire-like-7qutzwquu-k0986s-projects.vercel.app/like"

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

@bot.command(name="like", help="Send a like to a Free Fire UID")
async def like(ctx, uid: str):
    try:
        # Send initial response
        await ctx.send(f"Processing like request for UID: {uid}...")
        
        # Make API request
        response = requests.get(f"{API_URL}?uid={uid}")
        data = response.json()
        
        if response.status_code == 200:
            # Create embed for better presentation
            embed = discord.Embed(
                title="Like Request Result",
                color=discord.Color.green()
            )
            embed.add_field(name="Player", value=data.get("player", "Unknown"), inline=False)
            embed.add_field(name="Likes Before", value=str(data.get("likes_before", "N/A")), inline=True)
            embed.add_field(name="Likes After", value=str(data.get("likes_after", "N/A")), inline=True)
            embed.add_field(name="Likes Added", value=str(data.get("likes_added", 0)), inline=True)
            embed.set_footer(text=f"Server: {data.get('server_used', 'Unknown')}")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Failed to like UID {uid}. Error: {data.get('message', 'Unknown error')}")
            
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        await ctx.send(f"❌ Failed to connect to the API. Please try again later.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await ctx.send(f"❌ An unexpected error occurred. Please try again later.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please provide a UID. Usage: `!like <uid>`")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!like <uid>` to send likes.")
    else:
        logger.error(f"Command error: {str(error)}")
        await ctx.send("❌ An error occurred while processing your command.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("No Discord bot token found!")
        raise ValueError("DISCORD_BOT_TOKEN environment variable is required")
    
    bot.run(token)
