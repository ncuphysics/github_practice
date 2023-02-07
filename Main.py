from discord.ext          import commands
from pathlib              import Path
from datetime             import datetime
from User                 import User

import discord
import os

# intents = discord.Intents.default()
# intents.members = True
# intents.typing  = True
# intents.presences = True
# intents.message_content = True #v2

testing_guild = [597757976920588288, 1071431018701144165]
client = commands.Bot()

User_dict = {}  ##   {userid : userclass }


# tree = app_commands.CommandTree(client)

print("Start server")


@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.slash_command(name="checkin",description="check in",guild_ids=testing_guild)
async def checkin(ctx): 
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = User(ctx.author)

    if (await User_dict[ctx.author.id].checkin()):
        await ctx.respond(f"{ ctx.author.name} check_in !")
    else:  
        await ctx.respond(f"you didn't check out last time")

@client.slash_command(name="checkout",description="check out",guild_ids=testing_guild)
async def checkout(ctx): 
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = User(ctx.author)

    if (await User_dict[ctx.author.id].checkout()):
        await ctx.respond(f"{ ctx.author.name} check out !")
    else:
        await ctx.respond(f"No check in record!!")



DISCORDTOKEN = ''

client.run(DISCORDTOKEN)
