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

            result = await speech_to_text(this_file)
            print(user_id,":",result)
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
        await interaction.response.send_message('====== Stop recording ======')
        self.voice_channel.stop_recording()
        # await ctx.delete()
        # await self.text_channel 




async def speech_to_text(path):
    """"
    convert audio from .wav file to text using
     google speech recognition API.
    """
    # print(sr.__version__)
    r = sr.Recognizer() 
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 300,
        silence_thresh = sound.dBFS-14,
        keep_silence=100,
    )

    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = []

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            try:
                audio_listened = r.record(source)
                try:
                    text = r.recognize_google(audio_listened, language = 'zh-tw', show_all=True)
                    if text['alternative'][0]['confidence'] < 0.7:
                        text['alternative'][0]['transcript'] = "*inaudible*"
                    text = text['alternative'][0]['transcript']
                except sr.UnknownValueError as e:
                    text = "*inaudible*"
                else:                
                    whole_text.append(text)
            except:
                whole_text.append('')
                continue
    return whole_text


    # with sound as source:
    #     # r.adjust_for_ambient_noise(source, duration=0.5)
    #     # r.adjust_for_ambient_noise(source)
    #     audio = r.record(source)

    # return r.recognize_google(audio,language ='zh-tw')
    # print(r.recognize_google(audio, show_all=True))
    









if __name__ == "__main__":
    result = speech_to_text(r"D:\Carrer_hack\github_practice\recorded\1071431018701144165\23-02-09-00\518082603090182144.wav")
    # result = speech_to_text(r'output.wav')

    print(result)




