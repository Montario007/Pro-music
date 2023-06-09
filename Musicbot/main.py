import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

queues = {}  


playlists = {
    "gaming": ["relax.mp3", "song.mp3", "chill music.mp3"],
    "relax": ["relax1.mp3", "relax2.mp3", "relax3.mp3"],
    "chill music": ["chill1.mp3", "chill2.mp3", "chill3.mp3"]
}


@client.event
async def on_ready():
    print("The bot is ready")


@client.event
async def on_voice_state_update(member, before, after):
    
    if member.id == client.user.id and before.channel is not None and after.channel is None:
        guild_id = before.channel.guild.id
        await check_queue(guild_id)


async def check_queue(guild_id):
    if guild_id in queues:
        queue = queues[guild_id]
        if queue:
            voice_client = queue[0]["voice_client"]
            if not voice_client.is_playing() and not voice_client.is_paused():
                song = queue.pop(0)
                source = FFmpegPCMAudio(song["filename"])
                voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(check_queue(guild_id), client.loop))
                
                await asyncio.ensure_future(check_queue(guild_id))


@client.command()
async def hello(ctx):
    await ctx.send("HI")


@client.command()
async def playlistinfo(ctx):
    await ctx.send("Choose between these playlists to play: gaming, rap, hype")

@client.command()
async def gaminginfo(ctx):
    await ctx.send("playlist songs in [gaming]:(song,relax,chill music)")
@client.command()
async def hypeinfo(ctx):
    await ctx.send("playlist songs in [hype]:(song1,song 2,song 3)")

@client.command()
async def rapinfo(ctx):
    await ctx.send("playlist songs in [rap]:(song1,song2, song 3)")

@client.command()
async def bye(ctx):
    await ctx.send("See ya")


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        queues[ctx.guild.id] = []
        await ctx.send("Joined the voice channel")
    else:
        await ctx.send("You are not in a voice channel. You must be in a voice channel to run this command")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        guild_id = ctx.guild.id
        await ctx.guild.voice_client.disconnect()
        if guild_id in queues:
            del queues[guild_id]
        await ctx.send("Left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


@client.command(pass_context=True)
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("There is no audio playing in the voice channel")


@client.command(pass_context=True)
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("There is no song paused")




@client.command(pass_context=True)
async def play(ctx, arg):
    voice_client = ctx.guild.voice_client
    if arg in playlists:
        for song in playlists[arg]:
            source = FFmpegPCMAudio(song)
            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = []  
            queues[ctx.guild.id].append({"filename": song, "voice_client": voice_client})
        await ctx.send(f"{arg} playlist has been added to the queue")
        if not voice_client.is_playing() and not voice_client.is_paused():
            await check_queue(ctx.guild.id)
    else:
        song = arg + '.mp3'
        source = FFmpegPCMAudio(song)
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []  
        queues[ctx.guild.id].append({"filename": song, "voice_client": voice_client})
        await ctx.send(f"{arg} has been added to the queue")
        if not voice_client.is_playing() and not voice_client.is_paused():
            await check_queue(ctx.guild.id)


@client.command(pass_context=True)
async def queue(ctx, arg):
    song = arg + '.mp3'
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []  
    queues[ctx.guild.id].append({"filename": song, "voice_client": ctx.guild.voice_client})
    await ctx.send(f"{arg} has been added to the queue")

@client.command(pass_context=True)
async def queueinfo(ctx):
    if ctx.guild.id not in queues:
        await ctx.send("The queue is empty")
        return

    queue = queues[ctx.guild.id]
    if not queue:
        await ctx.send("The queue is empty")
        return

    message = "Current Queue:\n"
    for i, song in enumerate(queue):
        message += f"{i+1}. {song['filename'].replace('.mp3', '')}\n"
    await ctx.send(message)

@client.command(pass_context=True)
async def skip(ctx):
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel")
        return

    queue = queues.get(ctx.guild.id)
    if not queue:
        await ctx.send("The queue is empty")
        return

    ctx.voice_client.stop()
    await ctx.send("Skipped the current song")

    
    await check_queue(ctx.guild.id)

client.run("MTA4NDgyNTIwOTY5MDkxNDgzNg.GOTJqc.Dn76Sz7M41d2NIzsXTVrcxYLiXK87PEO2Epdfo")
 