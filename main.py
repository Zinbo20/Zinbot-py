import discord
from discord.utils import get
import os
import random
import asyncio
loop = asyncio.get_event_loop()
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import re
import urllib
from youtube_dl import YoutubeDL

players = {}
COR = 0xF7FE2E

client = discord.Client()

q = []
name = []
t = 2
i = 0

canal_voice = 0
canal_voice2 = 0

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

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
async def on_message(message):

    if message.content.startswith('*help'):
        embed_help = discord.Embed(colour=discord.Colour.blue())
        embed_help.set_author(name='Zinbot',
                              icon_url='https://i.imgur.com/To6Bkn2.jpg')
        embed_help.add_field(
            name='All commands',
            value=
            '*help*, *play*, *blitzcrank*, *zinbot*, *leave*, *clear*, *list*, *skip*',
            inline=False)

        await message.channel.send(embed=embed_help)

    elif message.content.startswith('*zinbot'):
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

    elif message.content.startswith('*blitzcrank'):
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

    elif message.content.startswith('*leave'):
        await message.guild.voice_client.disconnect()

    elif message.content.startswith('*clear'):
        q.clear()
        name.clear()

    elif message.content.startswith('*list'):
        embed_list = discord.Embed(colour=discord.Colour.blue())
        embed_list.add_field(name='Lista de Reprodução',
                             value=name,
                             inline=False)

        await message.channel.send(embed=embed_list)

    elif message.content.startswith('*skip'):
        global t
        t = 1
        await message.guild.voice_client.disconnect()
        canal = message.author.voice.channel
        await canal.connect()
        voice = get(client.voice_clients, guild=message.channel.guild)
        await asyncio.gather(queue(message,voice))
        await asyncio.gather(embed_musica(message, q[0]))

    elif message.content.startswith('*play'):

        global canal_voice, canal_voice2
        global x

        attachment = str(message.content)
        search = ""

        x = 1
        while True:
            msg = attachment.split()[x]
            search += msg + " "
            x = x + 1
            if x == len(attachment.split()):
                break

        msg = attachment.split()[1]

        search = search.replace(" ", "+")

        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        yt_url = "https://www.youtube.com/watch?v=" + video_ids[0]

        yt_url2 = "https://youtu.be/" + video_ids[0]

        canal = message.author.voice.channel

        voice = discord.utils.get(client.voice_clients,
                                  guild=message.author.guild)

        if voice == None:
            await canal.connect()
            canal_voice = message.author.voice.channel.id
            if (msg != yt_url and msg != yt_url2):
                await asyncio.gather(embed_musica(message, yt_url))
            await asyncio.gather(play(message, yt_url))
        else:
            canal_voice2 = message.author.voice.channel.id
            if canal_voice == canal_voice2:
                if (msg != yt_url and msg != yt_url2):
                    await asyncio.gather(embed_musica(message, yt_url))
                await asyncio.gather(play(message, yt_url))
            else:
                await message.channel.send(
                    "I'm already playing in other channel")


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


#play
async def play(message, yt_url):
    global t, q, v_title,thumnail_url

    q.append(yt_url)

    voice = get(client.voice_clients, guild=message.channel.guild)

    if (len(q) == 1):
        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(q.pop(0), download=False)
                t = info.get("duration", None)
                v_title = info.get('title', None)
                video_id = info.get("id", None)
                thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % video_id
                URL = info['formats'][0]['url']
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()

    if (len(q) >= 1):
        name.append(v_title)

        embed_add_track = discord.Embed(
        title="Added Track" ,
        colour= 000000)
        embed_add_track.add_field(name="Track: ", value= yt_url, inline=False)
        embed_add_track.add_field(name="Position: ", value= len(q), inline=False)
        embed_add_track.set_thumbnail(url=thumnail_url)
        await message.channel.send(embed=embed_add_track)

        await asyncio.gather(queue(message,voice))
    #play


async def queue(message,voice):
    global q, t, name, i,queue_title
    if i <= t:
        i = i + 1
        await asyncio.sleep(1)
    else:
        if not voice.is_playing():
            i = 0
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(q[0], download=False)
                URL = info['formats'][0]['url']
                t = info.get("duration", None)
                queue_title = info.get('title', None)
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()

    if voice.is_playing() and i == 0:
        embed_queue = discord.Embed(
        title="Started playing "+queue_title,
        url = q[0] ,
        colour=  000000)
        await message.channel.send(embed=embed_queue)
        q.pop(0)
        name.pop(0)

    if voice.is_playing() or len(q) >= 1:
        await asyncio.gather(queue(message,voice))
    elif i >= t:
        embed_track = discord.Embed(
        description='There are no more tracks',
        colour=discord.Colour.red())
        await message.channel.send(embed=embed_track)


client.run(os.getenv('TOKEN'))