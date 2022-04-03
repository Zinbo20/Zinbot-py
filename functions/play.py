import discord
from discord.utils import get
from discord import FFmpegPCMAudio
import re
import urllib
from youtube_dl import YoutubeDL
import asyncio
import unidecode 

client = discord.Client()

queue = []
name = []

canal_voice = 0
canal_voice2 = 0

bool_run = False

YDL_OPTIONS = {'cookiefile': 'cookies.txt','format': 'bestaudio', 'noplaylist': 'True'}

FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'
}

from functions import embed
from functions import playlist
from functions import fun_queue

async def comando_play(message,client2):
  global canal_voice, canal_voice2,client,queue
  client = client2
  msg = ""
  yt_url = ""

  attachment = str(message.content)
  search = ""

  if(len(attachment.split()) > 1):
    x = 1
    while True:
      msg = attachment.split()[x]
      search += msg + " "
      x = x + 1
      if x == len(attachment.split()):
        break

    outputString = unidecode.unidecode(search) 
    search = outputString

    msg = attachment.split()[1]

    if not msg.startswith('https://'):

      search = search.replace(" ", "+")

      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

      yt_url = "https://www.youtube.com/watch?v=" + video_ids[0]

    else:
      yt_url = attachment.split()[1]

    canal = message.author.voice.channel

    voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

    if voice == None:
      await canal.connect()
      canal_voice = message.author.voice.channel.id

      voice = discord.utils.get(client.voice_clients, guild=message.author.guild)
      #await message.channel.send(f"Joined **{canal}**")

      if not msg.startswith('https://') and not voice.is_playing():
          await asyncio.gather(embed.embed_musica(message, yt_url))
      if msg.startswith('https://youtube.com/playlist') or msg.startswith('https://www.youtube.com/playlist'):
        await asyncio.gather(playlist.playlist(message,yt_url,client2))
      else:
        await asyncio.gather(play(message, yt_url))
    else:
      canal_voice2 = message.author.voice.channel.id
      if canal_voice == canal_voice2:
          if not msg.startswith('https://') and not voice.is_playing():
            await asyncio.gather(embed.embed_musica(message, yt_url))
          if msg.startswith('https://youtube.com/playlist') or msg.startswith('https://www.youtube.com/playlist'):
              await asyncio.gather(playlist.playlist(message,yt_url,client2))
          else:
              await asyncio.gather(play(message, yt_url))
      else:
          await message.channel.send(
                    "I'm already playing in other channel")

  elif(len(attachment.split()) == 1):
    if queue:
      voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

      if voice == None:

        canal = message.author.voice.channel
        await canal.connect()

        voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

        await asyncio.gather(fun_queue.fun_queue(message,voice,client))
        
      else:
        embed_noq = discord.Embed(description='It is already playing',
        colour=discord.Colour.red())
        await message.channel.send(embed=embed_noq)
    else:
      embed_noq = discord.Embed(description='There is nothing to play',
      colour=discord.Colour.red())
      await message.channel.send(embed=embed_noq)

async def play(message, yt_url):
  global queue, name, v_title, client
  global bool_run
  
  if bool_run == True and len(queue) == 0:
    bool_run == False
  try:
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(yt_url, download=False)
      v_title = info.get('title', None)
  except Exception as e:
    print('\n')
    print('1- Exception is')
    print(e)
    print('\n')
  
  queue.append(yt_url)
  name.append(v_title)

  voice = get(client.voice_clients, guild=message.channel.guild)
  
  if len(queue) >= 1 and bool_run == True:
    await asyncio.gather(embed.embed_track(message,yt_url))

  if len(queue) >= 1 and bool_run == False:
    bool_run = True
    await asyncio.gather(fun_queue.fun_queue(message,voice,client))






async def add(message):
  global canal_voice, canal_voice2,queue,name
  msg = ""
  yt_url = ""

  attachment = str(message.content)
  search = ""

  print("msg=")
  print(len(attachment.split()))

  if(len(attachment.split()) > 1):
    x = 1
    while True:
      msg = attachment.split()[x]
      search += msg + " "
      x = x + 1
      if x == len(attachment.split()):
        break

    outputString = unidecode.unidecode(search) 
    search = outputString

    msg = attachment.split()[1]

    if not msg.startswith('https://'):

      search = search.replace(" ", "+")

      html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

      yt_url = "https://www.youtube.com/watch?v=" + video_ids[0]

    else:
      yt_url = attachment.split()[1]

    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(yt_url, download=False)
      v_title = info.get('title', None)

    if not msg.startswith('https://'):

      embed_queue = discord.Embed(title="Added Music " + v_title,
      url=yt_url,
      colour=000000)
      await message.channel.send(embed=embed_queue)
      queue.append(yt_url)
      name.append(v_title)

    elif msg.startswith('https://youtube.com/playlist'):
      await asyncio.gather(playlist.playlist(message,yt_url,client2))

    else:
      queue.append(yt_url)
      name.append(v_title)
        