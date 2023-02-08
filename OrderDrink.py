from datetime import datetime


import threading 
import asyncio
import discord
import time

class Drink_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="飲料品項"))
        self.add_item(discord.ui.InputText(label="客製化(甜度冰塊)", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="你的飲料")
        embed.add_field(name="飲料品項"        , value=self.children[0].value)
        embed.add_field(name="客製化(甜度冰塊)" , value=self.children[1].value)

        await interaction.user.send(embeds=[embed])
        await interaction.response.send_message(content='You have successfully order your drink, please check your message', ephemeral=True)


class OrderDrink(discord.ui.View):

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)


    @discord.ui.button(label="我要訂飲料!!", style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        # await interaction.user.send('Please enter the drink you want to drink')
        modal = Drink_modal(title='Please enter the drink you want to drink')
        await interaction.response.send_modal(modal)
        # await interaction.response.send(f"A drink order is initiated !!", view=self)
