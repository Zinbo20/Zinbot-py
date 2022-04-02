import discord
import asyncio

client = discord.Client()

msg = None

from functions import play
  
async def onreaction(reaction,user,client2):
  global msg,i,pag
  client = client2
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

      while x < len(play.name) and x < i*10:
        des += str(x+1)+': '+play.name[x]+'\n'
        x += 1

      page = discord.Embed (
        title = 'Page '+str(i)+'/'+str(pag),
        description = des,
        colour = discord.Colour.orange()
      )

      await msg.edit(embed=page)

      await reaction.remove(user)

async def list(message):
  global msg,pag,i
  des=''
  x=0
  i=1

  if(play.name):
    while x < len(play.name) and x < i*10:
      des += str(x+1)+': '+play.name[x]+'\n'
      x += 1

    pag = len(play.name)/10
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