import discord
import asyncio
from pytube import Playlist

client = discord.Client()

from functions import embed
from functions import fun_queue
from functions import play

async def playlist(message,yt_url,client2):
  client = client2

  if play.bool_run == True and len(play.queue) == 0:
    play.bool_run == False

  voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

  embed_loading = discord.Embed(description='Carregando Playlist...',
                                  colour=discord.Colour.blue())
  await message.channel.send(embed=embed_loading)

  p = Playlist(yt_url)

  print(f'Downloading: {p.title}')

  for url in p.video_urls:
    play.queue.append(url)

  for video in p.videos:
    play.name.append(video.title)

  await asyncio.gather(embed.embed_track(message,yt_url))
    
  if len(play.queue) > 1 and play.bool_run == False:
    await asyncio.gather(fun_queue.fun_queue(message,voice,client))