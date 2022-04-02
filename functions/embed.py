import discord
from youtube_dl import YoutubeDL
import os

client = discord.Client()

YDL_OPTIONS = {'cookiefile': 'cookies.txt','format': 'bestaudio', 'noplaylist': 'True'}

FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'
}

from functions import play

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
                                  value=len(play.queue),
                                  inline=False)
    #embed_add_track.add_field(name="Tempo: ", value= t, inline=False)
    embed_add_track.set_thumbnail(url=thumnail_url)
    await message.channel.send(embed=embed_add_track)

async def embed_zinbot(message):
  embed_zinbot = discord.Embed(
      title='Zinbot',
      description=
            'Zinbot é um robô com o tema inspirado em Blitzcrank de League of Legends.Suas funções alem de limpar Zaum, é tocar música, gerenciar o servidor e dar aquele puxão pro seu amigo entrar no jogo.',
      colour=discord.Colour.blue())
  embed_zinbot.set_footer(text='Baby Blitzcrank')
  embed_zinbot.set_image(url='https://i.imgur.com/To6Bkn2.jpg')
  embed_zinbot.set_thumbnail(url='https://i.imgur.com/NPYebgC.gif')
  embed_zinbot.set_author(name='Caique Leandro Tessaroto',icon_url='https://i.imgur.com/Aob5nfO.jpg')
  await message.channel.send(embed=embed_zinbot)

async def embed_feedback(message,client2):
  attachment = str(message.content)
  mensagem = ""
  client = client2
    
  x = 1
  while True:
    mensagem += attachment.split()[x] + " "
    x = x + 1
    if x == len(attachment.split()):
      break

  dev = await client.fetch_user(os.getenv('Dev.id'))

  embed_bug = discord.Embed(
        title='Feedback',
        description=
            mensagem,
            colour=discord.Colour.green())
  embed_bug.set_footer(text=message.guild)
  embed_bug.set_author(name=message.author.display_name,
icon_url=message.author.avatar_url)

  await dev.send(embed=embed_bug)

  embed=discord.Embed(description="Mensagem enviada para o desenvolvedor.", color=discord.Color.blue())
  await message.channel.send(embed=embed)