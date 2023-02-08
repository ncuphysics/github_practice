from datetime import datetime

import discord
import os


class StopRecordSave():
    def __init__(self,savefolder):
        self.savefolder = savefolder

    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
        recorded_users = [  # A list of recorded users
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]

        await sink.vc.disconnect()
        
        print(channel.id)

        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
        await channel.send(f"Finished recording audio for: \n{', '.join(recorded_users)}.", files=files) 


class StopRecordButton(discord.ui.View):
    def __init__(self, voice_channel, text_channel, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.voice_channel = voice_channel
        self.text_channel  = text_channel
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)

    @discord.ui.button(label="停止錄音", style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        self.voice_channel.stop_recording()
        # await ctx.delete()
        # await self.text_channel 

        await interaction.response.send_message('====== Stop recording ======')



