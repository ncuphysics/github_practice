from discord.commands     import Option
from discord.ext          import commands
from datetime             import datetime
from pathlib              import Path

import OrderDrink   as my_od # my class
import Record       as my_rd # my class
import User         as my_Us # my class

import discord
import time
import os

# pip install py-cord

testing_guild = [597757976920588288, 1071431018701144165]
client = commands.Bot()

User_dict   = {}  ##   {userid : userclass }k
orders      = {}
teams       = {}

RECORD_FOLDER = "recorded"
os.makedirs(RECORD_FOLDER, exist_ok=True)

TEAM_FILE_NAME = "teams.json"

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
async def order_drink(ctx,  timeout_min: Option(int, "Time out (min)", required = False, default = 5)):


    ## send menu
    await ctx.send('======= Menu =======')
    with open("menu.png", "rb") as fh:
        f = discord.File(fh, filename='menu.png')
    await ctx.send(file=f)



    print(f"[*] {ctx.author.name} initialize a drink order with timeout :",timeout_min )

    ## 按鈕
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
    del orders[ctx.author.id]



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


# 訂會議室
@client.slash_command(name="BookMeeting",description="Get users checkin record",guild_ids=testing_guild)
async def BookMeeting(ctx):
    
    ## check if user is a team leader, set a alarm to user



    await ctx.respond("====== BookMeeting ======")


############### team ############################################################


# 開始一個 team
# 提供所有人加入  

@client.slash_command(name="createteam",description="Create team",guild_ids=testing_guild)
async def createteam(ctx,  team_name: Option(str, "The team name", required = True)):
    ## Create a team  
    ## check if teamname exist

    await ctx.respond("====== Create team ======")

# 看check in out 紀錄
@client.slash_command(name="checkin_record",description="Get users checkin record",guild_ids=testing_guild)
async def checkin_record(ctx):
    ## check if user is any team leader
    ## choose each team


    await ctx.respond("====== checkin_record ======")


# 分派工作
@client.slash_command(name="teamwork",description="Get users checkin record",guild_ids=testing_guild)
async def teamwork(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== teamwork ======")


# 問團隊隊員現在的任務
@client.slash_command(name="member_current_tasks",description="Get users checkin record",guild_ids=testing_guild)
async def member_current_tasks(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== member_current_tasks ======")


@client.slash_command(name="teamkick",description="Get users checkin record",guild_ids=testing_guild)
async def teamkick(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== teamkick ======")



# 匿名回覆意見
@client.slash_command(name="opinion",description="Get users checkin record",guild_ids=testing_guild)
async def anonymousopinion(ctx):

    ## check if user in any team

    await ctx.respond("====== anonymousopinion ======")

############################################################

# get weather
@client.slash_command(name="weather",description="Get users checkin record",guild_ids=testing_guild)
async def weather(ctx):



    await ctx.respond("====== weather ======")



# get stock
@client.slash_command(name="stock",description="Get users checkin record",guild_ids=testing_guild)
async def stock(ctx):

    

    await ctx.respond("====== stock ======")


# get earthquake
@client.slash_command(name="earthquake",description="Get users checkin record",guild_ids=testing_guild)
async def earthquake(ctx):

    

    await ctx.respond("====== earthquake ======")



@client.slash_command(name="help",description="Shows help for the bot",guild_ids=testing_guild)
async def help(ctx):

    # embed = discord.Embed( title="Command", description="I'm a bot that could help you to works with your teams")

    # embed.add_field(name= "checkin"     , value="Check in"                 , inline=True)
    # embed.add_field(name= "checkout"    , value="Check out"                , inline=True)
    # embed.add_field(name= "order_drink" , value="Create a drink order"                  )
    # embed.add_field(name= "record"      , value="record yor meeting sound"              )

    text = """:sun_with_face:  **CHECKIN** :first_quarter_moon_with_face: **CHECKOUT**
\t\t-The Check in out function can provide automated registration, login and logout services, and provide detailed login records
\t\t-Allowing the team to manage and monitor user activities more easily.
\t\t-Allowing you to manage and monitor user activities more effectively.

:champagne_glass: **ORDER DRINK**
\t\t-You can create a drink order.
\t\t-Other users can enter what they want to drink.
\t\t-In the end you will receive all the drinks entered by the user

:speaking_head: **RECORD**
\t\t-You can record your meeting sound.
\t\t-You can get the summarize of the meeting.

:man_teacher: **CREATETEAM**
\t\t-You can create your own team.

:office_worker: **CHECKIN_RECORD**
\t\t-The team leader can check the team member check in-out record.

"""
    await ctx.send(text)


client.run('MTA3MTQ0MzU3NjgwMzgxOTUyMA.Gqahr6.rGVILocv83I6UBI-xENbgkgZnul9eI4LSsFSMM')
