import discord
from discord.ext import commands

client=commands.Bot(command_prefix=';')

@client.event
async def on_ready ():
    print('GG')

@client.event
async def on_member_join(member):
    await member.send(f'{member} zawitał/a na Ram Ranch!')

@client.event
async def on_member_remove(member):
    print(f'{member} opuścił/a Ram Ranch!')

@client.command()   
async def NakedCowboys(member):
    print('at Ram Ranch')

@client.command()   
async def clear(member, ile = 4 ):
    await member.channel.purge(limit = ile)#mem.channel zwraca obj channel

token=open("token.txt")#plik z tokenem
client.run(token.read())
print(token.read())
token.close()




