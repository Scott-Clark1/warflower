import os
import sys
import logging
from dotenv import load_dotenv

import discord
from keanu.client import WarflowerClient

load_dotenv()
handler = logging.FileHandler(filename='/home/ubuntu/logs/discord.log', encoding='utf-8', mode='w+')
logger = logging.getLogger('discord')
# handler = logging.StreamHandler(stream=sys.stdout)


admins = ["scottdoc", "john3361"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


warflower_client = WarflowerClient()

@client.event
async def on_ready():
  logger.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  author = message.author.name
  logger.info(f"REQUEST DETECTED FROM {author}")
  if author not in admins:
    return await message.channel.send(f"Permissions not found for {author}")

  if message.content.startswith('keanu'):

    # logging.info(message.global_name)
    terms = message.content.split()

    # LIST GAMES
    if len(terms) == 2 and terms[1].lower() == "list":
      msg = "Here are your available servers:"
      cfgs = warflower_client.list_configs()
      for c in cfgs:
        status = "[**ACTIVE**]" if cfgs[c] else ""
        msg += f"\n- {c} {status}"
      await message.channel.send(msg)

    # START SERVER
    elif terms[1].lower() == "start":
      res = warflower_client.start_server(terms[2])

      if res:
        await message.channel.send("Success!")
      else:
        await message.channel.send("FAILURE")

    # START SERVER
    elif terms[1].lower() == "stop":
      res = warflower_client.stop_server(terms[2])
      if res:
        await message.channel.send("Success!")
      else:
        await message.channel.send("FAILURE")
    else:
      msg = """Currently suppported commands:  
            - `keanu list`: list available server configurations  
            - `keanu start {serverid}`: start up a game server based off a config ID  
            - `keanu stop {serverid}`: stop a game server based off a config ID"""
      await message.channel.send(msg)

client.run(os.environ["DISCORD_TOKEN"], log_handler=handler, log_level=logging.INFO)
