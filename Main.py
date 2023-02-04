from discord.ext.commands import Bot
from discord.ext import commands
from pathlib import Path


import discord
import os

intents = discord.Intents.default()
intents.members = True
intents.typing  = True
intents.presences = True
intents.message_content = True #v2


help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = Bot('/',help_command = help_command,intents=intents)

print("Start server")


@client.event
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send(message.content)



DISCORDTOKEN =   os.getenv('DISCORD_TOKEN')

client.run(DISCORDTOKEN)
