import discord
from discord.ext import commands
import requests
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

API_URL = "https://freefire-like-7qutzwquu-k0986s-projects.vercel.app/like"

@bot.command(name="like", help="Send a like to a Free Fire UID")
async def like(ctx, uid: str):
    try:
        response = requests.get(f"{API_URL}?uid={uid}")
        data = response.json()
        if response.status_code == 200:
            player = data.get("player", "Unknown")
            likes_before = data.get("likes_before", "N/A")
            likes_after = data.get("likes_after", "N/A")
            await ctx.send(f"Player: {player}\\nLikes before: {likes_before}\\nLikes after: {likes_after}")
        else:
            await ctx.send(f"Failed to like UID {uid}. Response: {data}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(TOKEN)
