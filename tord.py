from random import sample, choice
from asyncio import TimeoutError
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='tord ')
token = ""
games = {}
no_game = "you don't have a game, type ``tord play [mention players]`` to start one"

with open('truth_questions.txt', 'r', encoding='utf-8') as f:
    truth_questions = f.read().splitlines()
with open('dare_questions.txt', 'r', encoding='utf-8') as f:
    dare_questions = f.read().splitlines()


@bot.command(aliases=('start', 'create', 'begin', 'make'), description='starts the game, example tord play @wentaas @lexxx')
async def play(ctx, *players: discord.Member):
    a = ctx.author
    if players:
        if a.id not in games:
            mentions = [a.mention]
            for player in players:
                if player.mention not in mentions:
                    mentions.append(player.mention)
            games[a.id] = mentions
            await ctx.send(f"{' '.join(mentions)} quick tutorial for yall:\njust type ``tord roll`` after answering and ``tord stop`` to end the game\n``tord add`` or ``tord remove`` to add/remove players\n"
                           "and if you want a question recommendation ``tord truth`` or ``tord dare``\nok enough talking **LET'S GOOO!**")
            await roll(ctx)
        else:
            await ctx.send("you already have a game, type ``tord stop`` to end it", delete_after=10)
    else:
        await ctx.send("so you use it like this ``tord play @wentaas @lexxx``", delete_after=30)


@bot.command(aliases=('quit', 'end', 'finish'), description='stops the game, usage: tord stop')
async def stop(ctx):
    a = ctx.author
    if a.id in games:
        games.pop(a.id)
        await ctx.send("i hope it was a good game, bye for now!!")
    else:
        await ctx.send(no_game, delete_after=10)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("couldn't find that member, try mentioning them")


@bot.command(description='adds players to the game, example: tord add @wentaas @lexxx')
async def add(ctx, *players: discord.Member):
    a = ctx.author
    if players:
        if a.id in games:
            mentions = games[a.id]
            added = []
            for player in players:
                if player.mention not in mentions:
                    mentions.append(player.mention)
                    added.append(player.mention)
            games[a.id] = mentions
            if added:
                await ctx.send(f"welcome {' '.join(added)} to the game!!")
            else:
                await ctx.send("i couldn't find anyone to add, are they already in the game?")
            await roll(ctx)
        else:
            await ctx.send(no_game, delete_after=10)
    else:
        await ctx.send("ok so you use it like this ``tord add @wentaas @lexxx``")


@bot.command(aliases=('kick', 'delete'), description='removes players from the game, example: tord remove @wentaas @lexxx')
async def remove(ctx, *players: discord.Member):
    a = ctx.author
    if players:
        if a.id in games:
            mentions = games[a.id]
            removed = []
            for player in players:
                if player != a:
                    if player.mention in mentions:
                        mentions.remove(player.mention)
                        removed.append(player.mention)
                else:
                    await ctx.send("you can't remove yourself from your own game, type ``tord stop`` for that")
                    break
            games[a.id] = mentions
            if removed:
                await ctx.send(f"bye {' '.join(removed)}, hope you had fun!!")
            else:
                await ctx.send("i couldn't find anyone to remove, are they not in the game anyway?")
            await roll(ctx)
        else:
            await ctx.send(no_game, delete_after=10)
    else:
        await ctx.send("ok so you use it like this ``tord remove @wentaas @lexxx``")


@bot.command(aliases=('again', 'new', 'continue'), description='picks who askes who again, usage: tord roll')
async def roll(ctx):
    a = ctx.author
    if a.id in games:
        try:
            choices = sample(games[a.id], 2)
            await ctx.send(f"{choices[0]} asks {choices[1]}")
        except ValueError:
            await ctx.send("you're probably the only one in game, aww are you getting lonely?")
    else:
        await ctx.send(no_game, delete_after=10)


@bot.command(description='sends a random truth question, usage: tord truth')
async def truth(ctx):
    await ctx.send(choice(truth_questions))


@bot.command(description='sends a random dare request, usage: tord dare', short_doc='sends a random dare request, usage: tord dare')
async def dare(ctx):
    await ctx.send(choice(dare_questions))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Truth or Dare, type tord play"))
    print("YAY LET'S PLAY!")

bot.run(token)
