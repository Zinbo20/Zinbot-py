import discord
from discord.utils import get
import os
import random
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import re
import urllib
from youtube_dl import YoutubeDL
from pytube import Playlist
import unidecode 

players = {}
COR = 0xF7FE2E

client = discord.Client()
Chave = '*'

q = []
name = []
t = 2
i = 1

queue_bool = 0

canal_voice = 0
canal_voice2 = 0

YDL_OPTIONS = {'cookiefile': 'cookies.txt','format': 'bestaudio', 'noplaylist': 'True'}

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


@client.event
async def on_ready():
    print(client.user.name)
    print("Bot online")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="*help"))

@client.event
async def on_reaction_add(reaction,user):
  global msg,i,pag
  des=''

  if msg != None:
    await asyncio.sleep(1)
    if(reaction.message.id == msg.id and user.name != client.user.name):

      if reaction.emoji == '⏮':
        i = 1
      elif reaction.emoji == '◀':
        if i > 1:
          i -= 1
      elif reaction.emoji == '▶':
        if i < pag:
          i += 1
      elif reaction.emoji == '⏭':
          i = pag

      x=(i-1)*10

      while x < len(name) and x < i*10:
        des += str(x+1)+': '+name[x]+'\n'
        x += 1

      page = discord.Embed (
        title = 'Page '+str(i)+'/'+str(pag),
        description = des,
        colour = discord.Colour.orange()
      )

      await msg.edit(embed=page)

      await reaction.remove(user)

@client.event
async def on_message(message):

  if message.content.startswith(Chave + 'help'):
    embed_help = discord.Embed(colour=discord.Colour.blue())
    embed_help.set_author(name='Zinbot',
                              icon_url='https://i.imgur.com/To6Bkn2.jpg')
    embed_help.add_field(name='General commands',
                             value='*help*, *ping*.',
                             inline=False)
    embed_help.add_field(
            name='Music commands',
            value=
            '*play*, *leave*, *clear*, *list*, *skip*, *stop*, *resume*, *pause*.',
            inline=False)
    embed_help.add_field(name='Specific commands',
                             value='*blitzcrank*, *zinbot*.',
                             inline=False)

    await message.channel.send(embed=embed_help)

  elif message.content.startswith(Chave + 'zinbot'):
    embed_zinbot = discord.Embed(
      title='Zinbot',
      description=
            'Zinbot é um robô com o tema inspirado em Blitzcrank de League of Legends.Suas funções alem de limpar Zaum, é tocar música, gerenciar o servidor e dar aquele puxão pro seu amigo entrar no jogo.',
      colour=discord.Colour.blue())
    embed_zinbot.set_footer(text='Baby Blitzcrank')
    embed_zinbot.set_image(url='https://i.imgur.com/To6Bkn2.jpg')
    embed_zinbot.set_thumbnail(url='https://i.imgur.com/NPYebgC.gif')
    embed_zinbot.set_author(name='Caique Leandro Tessaroto',
                                icon_url='https://i.imgur.com/Aob5nfO.jpg')
    await message.channel.send(embed=embed_zinbot)

  elif message.content.startswith(Chave + 'blitzcrank'):
    random_mensagem = [
      'Eu mantenho a concentração', 'O osso é uma péssima alternativa',
      'Estou tremendo de medo, pura carne', 'Seu vapor esta escapando',
      'Olha. Você está escapando', 'Exterminar. Exterminar',
      'A junta de rolamento do golem enferruja', 'A magia chama por mim',
      'Metal é mais duro do que a carne', 'Enquanto for preciso',
      'O tempo do homem chegou ao fim',
      'Eu coloquei o gol em golem. Esse foi o humor. Tem que ser golem para ser adequadamente engraçado'
      ]
    mensagem = random.choice(random_mensagem)
    await message.author.send(mensagem)

  elif message.content.startswith('Zinbot'):
    await message.channel.send("Demitido e pronto para servir.")

  elif message.content.startswith(Chave + 'leave'):
    await message.guild.voice_client.disconnect()

  elif message.content.startswith(Chave + 'clear'):
    q.clear()
    name.clear()

  elif message.content.startswith(Chave + 'list'):
    global msg,pag,i
    des=''
    x=0
    i=1

    if(q):
      while x < len(name) and x < i*10:
        des += str(x+1)+': '+name[x]+'\n'
        x += 1

      pag = len(name)/10
      if(pag > int(pag)):
        pag = int(pag)+1
      elif (pag == int(pag)):
        pag = int(pag)-1

      page = discord.Embed (
        title = 'Page '+str(i)+'/'+str(pag),
        description = des,
        colour = discord.Colour.orange()
      )

      msg = await message.channel.send(embed = page)

      await msg.add_reaction('⏮')
      await msg.add_reaction('◀')
      await msg.add_reaction('▶')
      await msg.add_reaction('⏭')
    
    else:
      embed_noq = discord.Embed(description='There are no Queue',
      colour=discord.Colour.red())
      await message.channel.send(embed=embed_noq)

  elif message.content.startswith(Chave + 'skip'):
    global t
    voice = get(client.voice_clients, guild=message.channel.guild)
    t = 1
    voice.stop()
    if not q:
      await asyncio.gather(timeout(message, voice))

  elif message.content.startswith(Chave + 'pause'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    if voice.is_playing():
        voice.pause()

  elif message.content.startswith(Chave + 'resume'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    if voice.is_paused():
        voice.resume()

  elif message.content.startswith(Chave + 'stop'):
    voice = get(client.voice_clients, guild=message.channel.guild)
    voice.stop()

  elif message.content.startswith(Chave + 'ping'):
    ping = client.latency * 1000
    if (ping < 40):
        emoji = ":green_circle:"
    elif (ping > 40 and ping <= 80):
        emoji = ":yellow_circle:"
    else:
        emoji = ":red_circle:"
    embed_ping = discord.Embed(description=emoji + " Ping: " +
                                    str(int(ping)) + "ms",
                                    colour=000000)
    await message.channel.send(embed=embed_ping)


  elif message.content.startswith(Chave + 'add'):
    global canal_voice, canal_voice2
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
        q.append(yt_url)
        name.append(v_title)

      elif msg.startswith('https://youtube.com/playlist'):
        await asyncio.gather(playlist(message, yt_url))

      else:
        q.append(yt_url)
        name.append(v_title)

  elif message.content.startswith(Chave + 'play'):
    global canal_voice, canal_voice2
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

        html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search)
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
            await asyncio.gather(embed_musica(message, yt_url))
        if msg.startswith('https://youtube.com/playlist') or msg.startswith('https://www.youtube.com/playlist'):
          await asyncio.gather(playlist(message, yt_url))
        else:
          await asyncio.gather(play(message, yt_url))
      else:
        canal_voice2 = message.author.voice.channel.id
        if canal_voice == canal_voice2:
            if not msg.startswith('https://') and not voice.is_playing():
                await asyncio.gather(embed_musica(message, yt_url))
            if msg.startswith('https://youtube.com/playlist') or msg.startswith('https://www.youtube.com/playlist'):
                await asyncio.gather(playlist(message, yt_url))
            else:
                await asyncio.gather(play(message, yt_url))
        else:
            await message.channel.send(
                    "I'm already playing in other channel")

    elif(len(attachment.split()) == 1):
      if q:
        voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

        if voice == None:

          canal = message.author.voice.channel
          await canal.connect()

          voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

          await asyncio.gather(queue(message, voice))
        else:
          embed_noq = discord.Embed(description='It is already playing',
          colour=discord.Colour.red())
          await message.channel.send(embed=embed_noq)
      else:
        embed_noq = discord.Embed(description='There is nothing to play',
        colour=discord.Colour.red())
        await message.channel.send(embed=embed_noq)


async def playlist(message, yt_url):
    global name, q

    voice = discord.utils.get(client.voice_clients, guild=message.author.guild)

    embed_loading = discord.Embed(description='Carregando Playlist...',
                                  colour=discord.Colour.blue())
    await message.channel.send(embed=embed_loading)

    p = Playlist(yt_url)

    print(f'Downloading: {p.title}')

    for url in p.video_urls:
      q.append(url)

    for video in p.videos:
      name.append(video.title)

    await asyncio.gather(embed_track(message, q[0]))

    if queue_bool == 0:
      await asyncio.gather(queue(message, voice))




async def embed_musica(message, yt_url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info_dict = ydl.extract_info(yt_url, download=False)
        video_id = info_dict.get("id", None)
        video_title = info_dict.get('title', None)

        thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id

        embed_music = discord.Embed(title=video_title,
        description='Playing ' + yt_url,
        colour=discord.Colour.green())

        embed_music.set_thumbnail(url=thumnail_url)
        await message.channel.send(embed=embed_music)

async def embed_track(message, yt_url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info_dict = ydl.extract_info(yt_url, download=False)
        video_id = info_dict.get("id", None)
        #video_title = info_dict.get('title', None)

        thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id
        embed_add_track = discord.Embed(title="Added Track",
                                        colour=discord.Colour.blue())
        embed_add_track.add_field(name="Track: ", value=yt_url, inline=False)
        embed_add_track.add_field(name="Position: ",
                                  value=len(q),
                                  inline=False)
        #embed_add_track.add_field(name="Tempo: ", value= t, inline=False)
        embed_add_track.set_thumbnail(url=thumnail_url)
        await message.channel.send(embed=embed_add_track)

#play
async def play(message, yt_url):
    global t, q, v_title, thumnail_url, queue_bool
    bool2 = 1

    q.append(yt_url)

    voice = get(client.voice_clients, guild=message.channel.guild)

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(yt_url, download=False)
        v_title = info.get('title', None)
        video_id = info.get("id", None)
        thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id

    if (bool2 == 1):
      if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(q.pop(0), download=False)
          URL = info['formats'][0]['url']
          t = info.get("duration", None)
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()

    if (len(q) >= 1 and queue_bool == 0):
        bool2 = 0

    if (len(q) >= 1):
        name.append(v_title)
        await asyncio.gather(embed_track(message, yt_url))

    if (bool2 == 0):
      await asyncio.gather(queue(message, voice))
    else:
      await asyncio.gather(timeout(message, voice))


async def queue(message,voice):
    global q, name, t, queue_bool
    queue_bool = 1

    while True:
      if voice.is_playing() or voice.is_paused():
        await asyncio.sleep(1)
      else:
        break

    await asyncio.sleep(1)
    voice = get(client.voice_clients, guild=message.channel.guild)

    if q:
      try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(q[0], download=False)
            t = info.get("duration", None)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
      except Exception as e:
        print('\n')
        print('Exception is')
        print(e)
        print('\n')

    if voice.is_playing():
        embed_queue = discord.Embed(title="Started playing " + name.pop(0),
                                    url=q.pop(0),
                                    colour=000000)
        await message.channel.send(embed=embed_queue)

    if not q:
      await asyncio.sleep(t)
      if not q:
        embed_track = discord.Embed(description='There are no more tracks',
                                    colour=discord.Colour.red())
        await message.channel.send(embed=embed_track)
        t = 1
        await asyncio.gather(timeout(message, voice))
        queue_bool = 0
        
    if q and voice != None:
      await asyncio.gather(queue(message, voice))



async def timeout(message, voice):
  while True:
    await asyncio.sleep(t+10)
    
    voice2 = discord.utils.get(client.voice_clients, guild=message.author.guild)
    
    if voice.is_playing() or voice.is_paused() or voice2 == None or q:
      break

    m=0
    while True:
      await asyncio.sleep(30)
      m += 1
      if m == 10*2 or voice.is_playing() or voice.is_paused() or voice2 == None or q:
        break
    
    voice2 = discord.utils.get(client.voice_clients, guild=message.author.guild)
    
    if voice.is_playing() or voice.is_paused() or voice2 == None or q:
      break
    else:
      embed_track = discord.Embed(
            description=
            'No tracks have been playing for the past 10 minutes, leaving :wave:',
            colour=discord.Colour.red())
      await message.channel.send(embed=embed_track)
      await voice.disconnect()
      break


client.run(os.getenv('TOKEN'))