import discord
import asyncio

client = discord.Client()

async def timeout(message, voice,client2):

  client = client2
  
  while True:
    await asyncio.sleep(10)
    
    voice2 = discord.utils.get(client.voice_clients, guild=message.author.guild)
    
    if voice.is_playing() or voice2 == None:
      break

    m=0
    while True:
      await asyncio.sleep(30)
      m += 1
      voice2 = discord.utils.get(client.voice_clients, guild=message.author.guild)
      if m == 10*2 or voice.is_playing() or voice2 == None:
        break
    
    if voice.is_playing() or voice2 == None:
      break
      
    else:
      embed_track = discord.Embed(
            description=
            'No tracks have been playing for the past 10 minutes, leaving :wave:',
            colour=discord.Colour.red())
      await message.channel.send(embed=embed_track)
      await voice.disconnect()
      break