import discord
from discord.ext import commands
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author.name == "Apollo" and "event" in message.embeds[0].title.lower():
        embed = message.embeds[0]
        data = {
            "event_title": embed.title,
            "description": embed.description,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open(f"logs/apollo_event_{datetime.utcnow().date()}.json", "a") as f:
            f.write(json.dumps(data) + "\n")
    await bot.process_commands(message)

bot.run("YOUR_BOT_TOKEN")
