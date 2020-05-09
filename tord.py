import discord
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="tord ")
token = "NzA4Nzc3OTUyOTc1OTEzMDEz.XrcTNg.vwRzxUISzp-UFyi1nwO7q-3zMb0"


@bot.commands()
async def play(ctx):
    await ctx.send("YAY mention everyone that's gonna play")
    try:
        m = await bot.wait_for('message', timeout=60)
        if m.author == ctx.author:
            if len(m.mentions) > 0:
                players = m.mentions
                if ctx.mention not in players:
                    players.append(ctx.mention)
                ctx.send("LET'S GO!")
            else:
                ctx.send(f"but you didn't mention anyone, are you confused? you just mention them")
    except asyncio.TimeoutError:
        ctx.send("you didn't tag anyone, don't you wanna play :(")
