import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl

client=commands.Bot(command_prefix=';')

@client.event
async def on_ready ():
    print('GG')

@client.event
async def on_client_join(ctx):
    await ctx.send(f'{ctx} zawitał/a na Ram Ranch!')

@client.event
async def on_client_remove(ctx):
    await ctx.send(f'{ctx} opuścił/a Ram Ranch!')

@client.command()   
async def NakedCowboys(ctx):
    await ctx.send('at Ram Ranch')

@client.command()   
async def clear(ctx, ile = 4 ):
    await ctx.channel.purge(limit = ile)#mem.channel zwraca obj channel


@client.command(pass_context = True,aliases =['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()        

    await ctx.send(f'bot jest na kanale {channel}')
    

@client.command(pass_context = True,aliases =['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'bot wyszedl z {channel}')
    else:
        print('nie ma go na kanale abywyjsc')
        await ctx.send(f'Niema mnie na {channel} boroku')


@client.command(pass_context=True,aliases =['p'])
async def play(ctx,url: str):#zakładamy komende z linkiem
    song_there = os.path.isfile("song.mp3")#jesli jest w dir
    
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError  as identifier:
        print('bot stara sie uzuwac grajaca muzyke.....')
        await ctx.send('Muzyka jescze gra!')
        return
    
    await ctx.send('Odtwarzam')

    voice = get(client.voice_clients,guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',#jest default wiec chyba ok??
        }]
    }    

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       print('download piosenk')
       ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            nazwa=file
            print(f'zmiana nazwy {file}\n')
            os.rename(file,"song.mp3")#zmieniam nazwe pliku aby go odczytywać bez większych trudnosci

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(f'{nazwa} nie gra'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.voice=0.07#głośność piosenki jak gra bazowo (0-1) 1 są zniekształcenia

    nnazwa=nazwa.rsplit("-",2)#aby ładnie wyglądało do napisania
    await ctx.send(f"Odtwarzanie{nazwa}")

@client.command(pass_context = True,aliases =['pa','pauza'])
async def pause(ctx):
    voice = get(client.voice_clients,guild =ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send('Muzyka zpałzowana')
    else:
        await ctx.send('nie ma co pałzować')

@client.command(pass_context = True,aliases =['r','rezume','res'])
async def resume(ctx):
    voice = get(client.voice_clients,guild =ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send('Muzyka resume')
    else:
        await ctx.send('nie ma co resumować')

@client.command(pass_context = True,aliases =['s'])
async def stop(ctx):
    voice = get(client.voice_clients,guild =ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Muzyka zastopowana')
    else:
        await ctx.send('nie ma co stopować')


token=open("token.txt")#plik z tokenem
client.run(token.read())
print(token.read())
token.close()




