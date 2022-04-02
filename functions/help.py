import discord

async def help(message):
  embed_help = discord.Embed(colour=discord.Colour.blue())
  embed_help.set_author(name='Zinbot',                    icon_url='https://i.imgur.com/To6Bkn2.jpg')
  
  embed_help.add_field(name='General commands',value='*help*, *ping*, *feedback*.',inline=False)
  
  embed_help.add_field(name='Music commands',value='*play*, *leave*, *clear*, *list*, *skip*, *resume*, *pause*.',inline=False)
  embed_help.add_field(name='Specific commands',value='*blitzcrank*, *zinbot*.',inline=False)

  await message.channel.send(embed=embed_help)