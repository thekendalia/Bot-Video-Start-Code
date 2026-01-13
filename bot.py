import discord
from discord import app_commands
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os


load_dotenv()
# ----- CONFIG -----
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK")

# ----- BOT SETUP -----
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# ----- SLASH COMMAND -----
@bot.tree.command(name="repeat", description="Repeat what I say back to me!")
@app_commands.describe(message="Message to repeat")
async def senddata(interaction: discord.Interaction, message: str):
    payload = {
        "user_id": interaction.user.id,
        "guild_id": interaction.guild.id if interaction.guild else None,
        "channel_id": str(interaction.channel.id),
        "message": message
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code in (200, 204):
        await interaction.response.send_message("Raw data sent to webhook!", ephemeral=True)
    else:
        await interaction.response.send_message(f"Failed to send webhook: {response.status_code}", ephemeral=True)

# ----- RUN BOT -----
bot.run(TOKEN)
