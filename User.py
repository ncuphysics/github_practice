from datetime import datetime

import discord

## handle every users data

class User:
    def __init__(self,user_ctx=None):
        self.user_ctx          = user_ctx
        self.check_stack       = []
        self.__check_in_record = []  # private
        self.__check_ou_record = []  # private

    async def checkout(self):

        ## forget check in
        if (len(self.check_stack)==0) :
            await self.user_ctx.send("No check in record!!")
            self.__check_in_record.append(None)
            return False
        else:
            this_check_time = datetime.now()
            checkin_time    = self.check_stack.pop()

            self.__check_ou_record.append(this_check_time)
            await self.user_ctx.send("you check out at "+ this_check_time.strftime("%m-%d %X"))
            return True
    async def checkin(self):

        ## forget check out
        if (len(self.check_stack)==1) :
            last_time = self.check_stack.pop() 
            await self.user_ctx.send("you didn't check out last time\n"+"check in record : "+last_time.strftime("%m-%d %X"))
            self.__check_ou_record.append(None)
            return False
        else:
            this_check_time  = datetime.now()
            self.check_stack = [this_check_time]

            self.__check_in_record.append(this_check_time)
            await self.user_ctx.send("you check in at "+this_check_time.strftime("%m-%d %X"))
            return True


    def get_user_check_in_record(self):
        return self.__check_in_record

    def get_user_check_in_record(self):
        return self.__check_out_record



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

class OrderTimeOutModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.timeout = 300
        self.ever_called =False
        self.add_item(discord.ui.InputText(label="訂飲料時間(s)"))

    async def callback(self, interaction: discord.Interaction):
        self.timeout   =  eval(self.children[0].value)
        # await interaction.response.send_message(content=f'You have set your timeout : {self.timeout}', ephemeral=True)
        self.ever_called = True
        
        await interaction.response.send_message(f"A drink order is initiated!! {self.timeout}[s]", view=OrderDrink(timeout=self.timeout))

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




if __name__ == '__main__':
    a = User()

