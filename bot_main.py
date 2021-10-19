import discord
from discord import voice_client
from discord.channel import TextChannel, VoiceChannel
from discord.ext import commands
from discord.voice_client import VoiceClient
import youtube_dl
import os
import asyncio

with open('TOKEN') as f:
    Token = f.readline()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
voice = False
players = {}



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        #print(data)
        
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
            video_url = data["webpage_url"]
        
        else:
            video_url = None
        

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), video_url










@client.event
async def on_ready():
    print('zalogowano jako {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(" -= "+message.content+" =- ")
    messageSplitted = (message.content).split(' ')
        

    if any(x == message.content[0] for x in {'.', '/', '!'}):    # sprawdzanie czy istanieje znak komendy
    
        if len(messageSplitted) == 1:

            if any(x == messageSplitted[0][1:].upper() for x in {'JOIN', 'DOLACZ', 'DOŁĄCZ', 'J'}):
                global voice
                voice = await (message.author).voice.channel.connect()



            elif any(x == messageSplitted[0][1:].upper() for x in {'LEAVE', 'L', 'W', 'WYJDZ', 'WYJDŹ', 'SPIERDALAJ', 'WYPIERDALAJ', 'FUCKOFF', 'EXIT', 'E', 'PAKÓJWALIZĘ', 'PAKÓJWALIZE', 'PAKOJWALIZE', 'SPIEPRZAJ'}):

                try:
                    voice.stop()
                except UnboundLocalError:
                    pass

                await voice.disconnect()



            elif any(x == messageSplitted[0][1:].upper() for x in {'PAUSE', 'WSTRZYMAJ', 'HALT'}):
                print("-- wstrzymywanie odtwarzania")
                voice.pause()



            elif any(x == messageSplitted[0][1:].upper() for x in {'RESUME', 'WZNÓW', 'WZNOW', 'KONTYNUUJ', 'CONTINUE'}):
                print("-- wznawianie odtwarzania")
                voice.resume()



            elif any(x == messageSplitted[0][1:].upper() for x in {'S', 'STOP'}):
                print("-- zatrzymywanie odtwarzania")
                voice.stop()



            else:
                pass

        elif len(messageSplitted) > 1:

            if any(x == messageSplitted[0][1:].upper() for x in {'P', 'PLAY', 'GRAJ', 'WŁĄCZ', 'WLACZ'}):

                try:
                    #global voice
                    voice = await (message.author).voice.channel.connect()
                except discord.errors.ClientException:
                    print("-- już połączony z kanałem głosowym")

                to_play = ' '.join(((message.content).split(' '))[1:])
                print("-- odtwarzanie " + to_play)
                player = await (YTDLSource.from_url(to_play, stream=True))
                print("   ",player[1])
                voice.play(player[0])
                link = str(player[1])
                
                if player[1] != None:
                    await TextChannel.send(content=link, self=client.get_channel(434656565413412868))



            else:
                pass
        
    else:
        pass





@client.event 
async def on_member_join(member):
    #print("ktoś dołączył do serwera")
    print(str(member) + 'dołączył do serwera')
    await TextChannel.send(content=f"@everyone Powitajcie @{member.name} na serwerze", self=client.get_channel(434656565413412868))

@client.event
async def on_member_remove(member):
    print(str(member) + 'opóścił serwer :\'\(')



client.run(Token)