import discord
import os
from dotenv import load_dotenv

from keanu.client import WarflowerClient

load_dotenv()

warflower_client = WarflowerClient()

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('keanu'):
    terms = message.content.split()
    if len(terms) == 2 and terms[1].lower() == "list":
      return warflower_client.list_configs()

if __name__ == "__main__":
  intents = discord.Intents.default()
  intents.message_content = True

  client = discord.Client(intents=intents)
