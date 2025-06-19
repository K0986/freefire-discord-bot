import discord
from discord.ext import commands
import os
import logging
import aiohttp
from aiohttp import ClientResponseError

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
        # Send initial response
        await ctx.send(f"Processing like request for UID: {uid}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}?uid={uid}", timeout=10) as response:
                try:
                    data = await response.json()
                    logger.info(f"API response data: {data}")
                except Exception as e:
                    logger.error(f"Failed to parse JSON response: {str(e)}")
                    await ctx.send("❌ Failed to parse response from API.")
                    return
                
                if response.status == 200:
                    # Create embed for better presentation
                    embed = discord.Embed(
                        title="Like Request Result",
                        description="Your like has been sent successfully!",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Player", value=data.get("player", "Unknown"), inline=False)
                    embed.add_field(name="Likes Before", value=str(data.get("likes_before", "N/A")), inline=True)
                    embed.add_field(name="Likes After", value=str(data.get("likes_after", "N/A")), inline=True)
                    embed.add_field(name="Likes Added", value=str(data.get("likes_added", 0)), inline=True)
                    embed.set_footer(text=f"Server: {data.get('server_used', 'Unknown')}")
                    embed.set_thumbnail(url="https://images.pexels.com/photos/256381/pexels-photo-256381.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
                    
                    await ctx.send(embed=embed)
                else:
                    logger.error(f"API returned error status {response.status}: {data}")
                    await ctx.send(f"❌ Failed to like UID {uid}. Error: {data.get('message', 'Unknown error')}")
                    
    except ClientResponseError as e:
        if e.status == 403:
            logger.error(f"Permission error: {str(e)}")
            await ctx.send("❌ Bot lacks the required permissions to perform this action. Please check the bot's permissions in your server.")
        else:
            logger.error(f"API request failed: {str(e)}")
            await ctx.send(f"❌ Failed to connect to the API. Please try again later.")
    except aiohttp.ClientError as e:
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
