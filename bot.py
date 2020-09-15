import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl
import shutil

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

    def check_que():
        queueInfile = os.path.isdir('./queue')
        if queueInfile is True:
            dir = os.path.abspath(os.path.realpath("queue"))
            lenght = len(os.listdir(dir))
            wQue = lenght -1
            try:
                queFile = os.listdir(dir)[0]
            except :
                print('nnie ma piosenek czyszcze que')
                queues.clear()
                return

            queFile=os.path.isdir('./queue')#sprawdzam cz jescze dlaje nie mam
            try:
                queFolder = "./queue"
                if queFile is True:
                    shutil.rmtree(queFolder)
                    print('rip stary folder que')
            except:
                print('nie ma folderu que')

            mainLoc = os.path.dirname(os.path.realpath(__file__))
            songPath = os.path.abspath(os.path.realpath('queue')+"\\"+queFile)
            if lenght !=0:
                print("w kolejce {wQue}")# na potem await ctx.send('w kolejce {wQue}') ale czy to dobry pomysł?
                song_there=os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(songPath,mainLoc)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file,'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:check_que())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.voice=0.07#głośność piosenki jak gra bazowo (0-1) 1 są zniekształcenia
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('koniec kolejki')


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

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:check_que)
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

    queues.clear()

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Muzyka zastopowana')
    else:
        await ctx.send('nie ma co stopować')

queues={}#pomocnicze do przechowania

@client.command(pass_context = True,aliases =['que','q'])
async def queue(ctx, url: str):
    queueInfile=os.path.isdir('./queue')
    if queueInfile is False:
        os.mkdir('queue')
    dir = os.path.abspath(os.path.realpath('queue'))#powinno sie dostac do que
    num = len(os.listdir(dir))#ile w que
    num +=1 #bo dodaje nowe
    addQue = True
    while addQue:#sprawdzam czy juz nie ma w kolejce
        if num in queues:
            num+=1
        else:
            addQue = False
            queues[num] = num

    quePath = os.path.abspath(os.path.realpath('queue')+f'\song{num}.%(ext)s'
    )

    ydl_opts = {
        'format':'bestaudio/best',
        'outtmpl':quePath,
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',#jest default wiec chyba ok??
        }]
    }    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       print('download piosenk')
       ydl.download([url])

    await ctx.send('Dodano '+str(num)+' do kolejki')


token=open("token.txt")#plik z tokenem
client.run(token.read())
print(token.read())
token.close()




