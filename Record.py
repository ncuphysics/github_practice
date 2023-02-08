from datetime       import datetime
from pydub          import AudioSegment
from pydub.playback import play
from pydub.silence  import split_on_silence

import speech_recognition as sr
import discord
import os


class StopRecordSave():
    def __init__(self,savefolder):
        self.savefolder = savefolder
        os.makedirs(savefolder,exist_ok=True)

    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
        recorded_users = [  # A list of recorded users
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]

        await sink.vc.disconnect()
            
        day_folder =  os.path.join(self.savefolder, datetime.now().strftime('%y-%m-%d-%H'))
        os.makedirs(day_folder,exist_ok=True)

        for user_id, audio in sink.audio_data.items():
            this_file = os.path.join(day_folder,f'{user_id}.wav')

            audio = AudioSegment.from_raw(audio.file, sample_width=2,frame_rate=48000,channels=2)
            audio.export(this_file, format='wav')

            speech_to_text(this_file)
            # speech_to_tex(a)
        # discordfiles = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
        # await channel.send(f"Finished recording audio for: \n{', '.join(recorded_users)}", files=discordfiles) 




# 停止按鈕

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



def speech_to_text(path):
    """"
    convert audio from .wav file to text using
     google speech recognition API.
    """
    # print(sr.__version__)
    r = sr.Recognizer() 
    sound = sr.AudioFile(path)
    # print(sr.Microphone.list_microphone_names()) # sr.Microphone(device_index=0)
    with sound as source:
        # r.adjust_for_ambient_noise(source, duration=0.5)
        # r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    return r.recognize_google(audio,language ='zh-tw', show_all=True)
    # print(r.recognize_google(audio, show_all=True))
    









if __name__ == "__main__":
    result = speech_to_text(r'recorded\597757976920588288\23-02-08-23\518082603090182144.wav')
    # result = speech_to_text(r'output.wav')

    print(result)