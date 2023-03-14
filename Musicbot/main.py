import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = True  # Add this line to include the GUILD_MESSAGE_TYPING intent
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("the bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("joined")

@client.command()
async def gg(ctx):
    await ctx.send("see ya")

@client.command(pass_context= True)
async def join(ctx):
    if (ctx.author.voice):
        channel=ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("you are not in a voice channel, you must be in a voice channel to run this command")

@client.command(pass_context= True)
async def leave (ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")
















client.run("MTA4NDgyNTIwOTY5MDkxNDgzNg.GOTJqc.Dn76Sz7M41d2NIzsXTVrcxYLiXK87PEO2Epdfo")