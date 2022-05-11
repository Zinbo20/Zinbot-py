import discord
import os
import asyncio
import random
from discord.utils import get

from urllib.error import ContentTooShortError

import sys

client = discord.Client()
Chave = '*'


class VoiceError(Exception):
  print(Exception)
  pass


class YTDLError(Exception):
  print(Exception)
  pass
  

@client.event
async def on_ready():
  print(client.user.name)
  print("Bot online")
  
  await client.change_presence(activity=discord.Activity(
type=discord.ActivityType.listening, name="*help"))

from functions import list

@client.event
async def on_reaction_add(reaction,user):
  await asyncio.gather(list.onreaction(reaction,user,client))

from functions import help
from functions import play
from functions import embed

@client.event
async def on_message(message):

  if message.content.startswith(Chave + 'help'):
    await asyncio.gather(help.help(message))

  elif message.content.startswith(Chave + 'restart'):
    sys.exit()

  elif message.content.startswith(Chave + 'list'):
    await asyncio.gather(list.list(message))

  elif message.content.startswith(Chave + 'play'):
    try:
      await asyncio.gather(play.comando_play(message,client))
    except ContentTooShortError as e:
      print('\n')
      print('all play Exception is')
      print(e)
      print('\n')

  elif message.content.startswith(Chave + 'zinbot'):
    await asyncio.gather(embed.embed_zinbot(message))

  elif message.content.startswith(Chave + 'blitzcrank'):
    random_mensagem = ['Eu mantenho a concentração', 'O osso é uma péssima alternativa','Estou tremendo de medo, pura carne', 'Seu vapor esta escapando','Olha. Você está escapando', 'Exterminar. Exterminar','A junta de rolamento do golem enferruja', 'A magia chama por mim','Metal é mais duro do que a carne', 'Enquanto for preciso','O tempo do homem chegou ao fim','Eu coloquei o gol em golem. Esse foi o humor. Tem que ser golem para ser adequadamente engraçado']
    mensagem = random.choice(random_mensagem)
    await message.author.send(mensagem)

  elif message.content.startswith('Zinbot'):
    await message.channel.send("Demitido e pronto para servir.")

  elif message.content.startswith(Chave + 'leave'):
    play.bool_run = False
    await message.guild.voice_client.disconnect()

  elif message.content.startswith(Chave + 'clear'):
    play.queue.clear()
    play.name.clear()

  elif message.content.startswith(Chave + 'feedback'):
    await asyncio.gather(embed.embed_feedback(message,client))

  elif message.content.startswith(Chave + 'skip'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    voice.stop()

  elif message.content.startswith(Chave + 'pause'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    if voice.is_playing():
        voice.pause()

  elif message.content.startswith(Chave + 'resume'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    if voice.is_paused():
        voice.resume()

  elif message.content.startswith(Chave + 'ping'):
    ping = client.latency * 1000
    if (ping < 40):
      emoji = ":green_circle:"
    elif (ping > 40 and ping <= 80):
      emoji = ":yellow_circle:"
    else:
      emoji = ":red_circle:"
    embed_ping = discord.Embed(description=emoji+"Ping: "+str(int(ping)) + "ms",colour=000000)
    await message.channel.send(embed=embed_ping)

  elif message.content.startswith(Chave + 'add'):
    await asyncio.gather(play.add(message))
    

client.run(os.getenv('TOKEN'))