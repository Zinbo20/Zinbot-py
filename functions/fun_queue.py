import discord
from discord.utils import get
import asyncio
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

client = discord.Client()


class VoiceError(Exception):
  print("Print on Queue VoiceError Exception: ")
  print(Exception)
  pass


class YTDLError(Exception):
  print("print on Queue YTDLError Exception: ")
  print(Exception)
  pass

  

YDL_OPTIONS = {'cookiefile': 'cookies.txt','format': 'bestaudio', 'noplaylist': 'True'}

FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'
}

from functions import timeout
from functions import play

async def fun_queue(message,voice,client2):
  #print("\nentrou queue\n")

  client = client2

  await asyncio.sleep(1)
  voice = get(client.voice_clients, guild=message.channel.guild)

  if not voice.is_playing():
    if play.queue:
      try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(play.queue[0], download=False)
          tempo = info.get("duration", None)
          URL = info['formats'][0]['url']
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()
      except Exception as e:
        print('\n')
        print('2- Exception is')
        print(e)
        print('\n')

  if voice.is_playing():
    embed_queue = discord.Embed(title="Started playing " +      play.name.pop(0),
    url=play.queue.pop(0),
    colour=000000)
    await message.channel.send(embed=embed_queue)

  while True:
    if voice.is_playing() or voice.is_paused():
      await asyncio.sleep(1)
      if voice.is_paused():
        print("\npause\n")
    else:
      break

  if not play.queue:
    embed_track = discord.Embed(description='There are no       more tracks',colour=discord.Colour.red())
    await message.channel.send(embed=embed_track)
    await asyncio.gather(timeout.timeout(message,voice,client))

  if play.queue and voice != None:
    await asyncio.gather(fun_queue(message,voice,client))
  #else:
  #  play.bool_run = True