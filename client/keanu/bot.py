import discord
import os
from dotenv import load_dotenv
load_dotenv()

from keanu.client import WarflowerClient


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


warflower_client = WarflowerClient()

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('keanu'):
    print("REQUEST DETECTED")
    terms = message.content.split()
    if len(terms) == 2 and terms[1].lower() == "list":
      msg = "Here are your available servers:"
      cfgs = warflower_client.list_configs()
      for c in cfgs:
        status = "*[ACTIVE]*" if cfgs[c] else ""
        msg = msg + f"\n\t- {c} " + status
      await message.channel.send(msg)

client.run(os.environ["DISCORD_TOKEN"])
