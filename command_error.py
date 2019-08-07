import discord
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run("NjA2ODkzODc4MDA3ODI0NDIx.XUq4RQ.G8EDgNokVR00h1g8vNOGI-aboQQ")