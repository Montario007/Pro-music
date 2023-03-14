import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("the bot is ready")

@client.command()
async def join(ctx):
    await ctx.send("joined")

client.run("MTA4NDgyNTIwOTY5MDkxNDgzNg.GOTJqc.Dn76Sz7M41d2NIzsXTVrcxYLiXK87PEO2Epdfo")