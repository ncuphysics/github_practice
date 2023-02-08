from discord.commands     import Option
from discord.ext          import commands
from OrderDrink           import *
from datetime             import datetime
from pathlib              import Path
from User                 import *

import discord
import time
import os

# intents = discord.Intents.default()
# intents.members = True
# intents.typing  = True
# intents.presences = True
# intents.message_content = True #v2

testing_guild = [597757976920588288, 1071431018701144165]
client = commands.Bot()

User_dict = {}  ##   {userid : userclass }

print("Start server")

@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.slash_command(name="checkin",description="check in",guild_ids=testing_guild)
async def checkin(ctx): 
    print(f'[*] {ctx.author.name} try to check in')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = User(ctx.author)

    if (await User_dict[ctx.author.id].checkin()):
        await ctx.respond(f"{ ctx.author.name} check_in !")
    else:  
        await ctx.respond(f"you didn't check out last time")



@client.slash_command(name="checkout",description="check out",guild_ids=testing_guild)
async def checkout(ctx): 
    print(f'[*] {ctx.author.name} try to check out')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = User(ctx.author)

    if (await User_dict[ctx.author.id].checkout()):
        await ctx.respond(f"{ ctx.author.name} check out !")
    else:
        await ctx.respond(f"No check in record!!")


@client.slash_command(name="order_drink",description="Order a drink",guild_ids=testing_guild)
async def order_drink(ctx,  timeout: Option(int, "Time out (must be a integer)", required = False, default =None)):
    await ctx.send('======= Menu =======')
    with open("menu.png", "rb") as fh:
        f = discord.File(fh, filename='menu.png')
    await ctx.send(file=f)
    print(f"[*] {ctx.author.name} initialize a drink order with timeout :",timeout )
    await ctx.response.send_message(f"@everyone!!  {ctx.author.mention} open a drink order", view=OrderDrink(timeout=timeout))


DISCORDTOKEN = ''

client.run(DISCORDTOKEN)
