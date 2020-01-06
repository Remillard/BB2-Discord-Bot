#! python3
# See https://realpython.com/how-to-make-a-discord-bot-python/
import os
import discord
import logging

logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(token)
