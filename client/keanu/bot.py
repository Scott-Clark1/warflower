import os
import sys
import logging
from dotenv import load_dotenv

import discord
from keanu.client import WarflowerClient

load_dotenv()
handler = logging.FileHandler(filename='/home/warflower/logs/discord.log', encoding='utf-8', mode='w+')
logger = logging.getLogger('discord')

admins = os.environ["ADMINS"].split(',')

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

  message_str = message.content.lower()
  if message_str.startswith('keanu'):
    author = message.author.name
    logger.info(f"REQUEST DETECTED FROM {author}")
    if author not in admins:
      return await message.channel.send(f"Permissions not found for {author}")

    # logging.info(message.global_name)
    terms = message_str.split()

    cmd = terms[1]

    # LIST GAMES
    if cmd == "list" or cmd == "status":
      if len(terms) < 3 or terms[2] == "configs":
        msg = "Here are your available server configurations (+ means active, - means offline):\n```diff"
        cfgs = warflower_client.list_configs()
        for c in cfgs:
          status = "+ " if cfgs.get(c, 0) else "- "
          msg += f"\n{status} {c}"
        msg += "```"
      elif terms[2] == "games":
        msg = "Here are your available games: ```"
        cfgs = warflower_client.list_games()
        for c in cfgs:
          msg += f"\n{c}"
        msg += "```"
      else:
        return await message.channel.send("What?")
      await message.channel.send(msg)

    # START SERVER
    elif cmd == "start":
      await message.channel.send("Lookin into it")
      res = warflower_client.start_server(terms[2])

      if res:
        await message.channel.send(f"`{terms[2]}`: I'm thinkin I'm back!")
      else:
        await message.channel.send("Unhandled exception")

    # START SERVER
    elif cmd == "stop":
      await message.channel.send("Lookin into it")
      res = warflower_client.stop_server(terms[2])
      if res:
        await message.channel.send(f"`{terms[2]}`'s gotta go down. It's gotta be that way.")
      else:
        await message.channel.send("Unhandled exception")
    else:
      msg = """Currently suppported commands:  
            - `keanu list`: list available server configurations  
            - `keanu start {config}`: start up a game server based off a config  
            - `keanu stop {config}`: stop a game server based off a config"""
      await message.channel.send(msg)

client.run(os.environ["DISCORD_TOKEN"], log_handler=handler, log_level=logging.INFO)
