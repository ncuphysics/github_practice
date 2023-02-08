from discord.commands     import Option
from discord.ext          import commands
from datetime             import datetime
from pathlib              import Path

import OrderDrink   as my_od
import Record       as my_rd
import User         as my_Us

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

User_dict   = {}  ##   {userid : userclass }k
orders      = {}

RECORD_FOLDER = "recorded"
os.makedirs(RECORD_FOLDER, exist_ok=True)

print("Start server")

@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.slash_command(name="checkin",description="check in",guild_ids=testing_guild)
async def checkin(ctx): 
    print(f'[*] {ctx.author.name} try to check in')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

    if (await User_dict[ctx.author.id].checkin()):
        await ctx.respond(f"{ ctx.author.name} check_in !")
    else:  
        await ctx.respond(f"you didn't check out last time")



@client.slash_command(name="checkout",description="check out",guild_ids=testing_guild)
async def checkout(ctx): 
    print(f'[*] {ctx.author.name} try to check out')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

    if (await User_dict[ctx.author.id].checkout()):
        await ctx.respond(f"{ ctx.author.name} check out !")
    else:
        await ctx.respond(f"No check in record!!")


@client.slash_command(name="order_drink",description="Order a drink (default 5 minute time out)",guild_ids=testing_guild)
async def order_drink(ctx,  timeout_min: Option(int, "Time out (s)", required = False, default = 5)):
    await ctx.send('======= Menu =======')
    with open("menu.png", "rb") as fh:
        f = discord.File(fh, filename='menu.png')
    await ctx.send(file=f)

    print(f"[*] {ctx.author.name} initialize a drink order with timeout :",timeout_min )
    this_order = my_od.OrderDrink(author = ctx.author, timeout=timeout_min*60)
    orders[ctx.author.id] = this_order

    await ctx.response.send_message(f"{ctx.author.mention} :exclamation: You can use a :stop_button: /stop_order_drink :stop_button:  command to close the order anytime you want.", ephemeral=True)
    await ctx.send(f"@everyone!!  {ctx.author.mention} open a drink order", view=this_order)


@client.slash_command(name="stop_order_drink",description="Stop the drink order",guild_ids=testing_guild)
async def stop_order_drink(ctx):
    if (ctx.author.id not in orders):
        await ctx.response.send_message('You didn\'t open any drink order',ephemeral=True)
    await orders[ctx.author.id].on_timeout()
    await ctx.response.send_message(f"You have stop the order", ephemeral=True)



@client.slash_command(name="record",description="Start a record",guild_ids=testing_guild)
async def record(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
        return
    vc = await voice.channel.connect()
    # connections.update({ctx.guild.id: vc})

    SRS = my_rd.StopRecordSave(os.path.join(RECORD_FOLDER,str(ctx.guild.id)))

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        # discord.Sink(encoding='wav', filters={'time': 0}),
        SRS.once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )

    await ctx.respond("====== Start recording ====== :speaking_head: :speech_balloon:\n",view=my_rd.StopRecordButton(voice_channel=vc,text_channel=ctx.channel,timeout=None))



@client.slash_command(name="help",description="Shows help for the bot",guild_ids=testing_guild)
async def help(ctx):

    embed = discord.Embed( title="你的飲料", description="I'm a bot that could help you to works with your teams")

    embed.add_field(name= "checkin"     , value="Check in"                 , inline=True)
    embed.add_field(name= "checkout"    , value="Check out"                , inline=True)
    embed.add_field(name= "order_drink" , value="Create a drink order"                  )
    embed.add_field(name= "record"      , value="record yor meeting sound"              )

    await ctx.send(embed=embed)



DISCORDTOKEN = 'MTA3MTQ0MzU3NjgwMzgxOTUyMA.GFU0x0.ulgLDgJVYCIRpF4CSYiRnfI5-MtmhdXFpJcPjA'



client.run(DISCORDTOKEN)
