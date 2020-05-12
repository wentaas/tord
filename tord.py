from random import sample, choice
from asyncio import TimeoutError
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='tord ')
token = ""
games = {}

with open('truth_questions.txt', 'r', encoding='utf-8') as f:
    truth_questions = f.read().splitlines()
with open('dare_questions.txt', 'r', encoding='utf-8') as f:
    dare_questions = f.read().splitlines()


async def roll(c, a):
    if a.id in games:
        choices = sample(games[a.id], len(games[a.id]))
        await c.send(f"{choices[0]} asks {choices[1]}")


# async def game(c, a, players=[], rem=False):
#     try:
#         msg = await bot.wait_for('message', timeout=120)
#         if msg.author == a:
#             print(a)
#             if len(msg.mentions) > 0:
#                 mentions = msg.mentions
#                 print(mentions)
#                 if rem:
#                     added = []
#                     not_added = []
#                     for name in mentions:
#                         if name.mention in players:
#                             added.append(name.mention)
#                             players.pop(name.mention)
#                         else:
#                             not_added.append(name.mention)
#                     await c.send(f"{' '.join(added)} removed from the game, see you again!!")
#                     if not_added:
#                         if len(not_added) > 1:
#                             await c.send(f"{' '.join(not_added)} weren't in the game anyway")
#                         else:
#                             await c.send(f"{' '.join(not_added)} wasn't in the game anyway")
#                 else:
#                     if not players:
#                         await c.send("type ``roll`` after answering and ``tord stop`` to end the game\n``tord add`` or ``tord remove`` to add/remove players"
#                                      "\n``tord truth`` or ``tord dare`` for a question recommendation\nok enough talking LET'S GOOO!")
#                         players.append(a.mention)
#                     for name in mentions:
#                         if name.mention not in players:
#                             players.append(name.mention)
#                     await c.send(f"{' '.join(players)} in the game!")
#                 games[a.id] = players
#                 await roll(c, a)
#             else:
#                 await c.send(f"but you didn't mention anyone, are you confused? you just mention them\nuse the command again please", delete_after=10)
#     except TimeoutError:
#         await c.send("you didn't tag anyone, don't you wanna play :(", delete_after=10)
#
#
# @bot.event
# async def on_message(m):
#     t = m.content.lower()
#     a = m.author
#     c = m.channel
#     if t.startswith(('tord play', 'tord start', 'tord create', 'tord begin', 'tord make')):
#         if a.id not in games:
#             await c.send("YAY!! mention everyone you wanna play with")
#             await game(c, a)
#         else:
#             await c.send(f"you already have a game, type ``tord stop`` to end it", delete_after=10)
#     if t.startswith(('tord stop', 'tord quit', 'tord end', 'tord add', 'tord join', 'tord remove', 'tord kick')):
#         if a.id in games:
#             if t.startswith(('tord stop', 'tord quit', 'tord end')):
#                 games.pop(a.id)
#                 await c.send("i hope it was a good game, bye for now!!")
#             elif t.startswith(('tord add', 'tord join', 'tord remove')):
#                 await c.send("ooo!! mention everyone you wanna add")
#                 await game(c, a, games[a.id])
#             elif t.startswith(('tord remove', 'tord kick')):
#                 await c.send("aww ok, mention everyone you wanna remove")
#                 await game(c, a, games[a.id], True)
#     elif t.startswith('tord truth'):
#         await c.send(choice(truth_questions))
#     elif t.startswith('tord dare'):
#         await c.send(choice(dare_questions))
#     elif t == 'roll':
#         await roll(c, a)


@bot.command(aliases=('start', 'create', 'begin', 'make'), description='starts the game, example: tord play @wentaas @lexxx')
async def play(ctx, *players: discord.Member):
    if players:
        a = ctx.author
        if a.id not in games:
            mentions = [a.mention]
            for player in players:
                if player.mention not in mentions:
                    mentions.append(player.mention)
            games[a.id] = mentions
            await ctx.send("type ``roll`` after answering and ``tord stop`` to end the game\n``tord add`` or ``tord remove`` to add/remove players"
                           "\n``tord truth`` or ``tord dare`` for a question recommendation\nok enough talking LET'S GOOO!")
            await roll(ctx.channel, a)
        else:
            await ctx.send("you already have a game, type ``tord stop`` to end it", delete_after=10)
    else:
        await ctx.send("so you use it like ``tord play @wentaas @alyyy``", delete_after=30)


@bot.command(aliases=('stop', 'quit', 'end', 'add', 'join', 'remove', 'kick'), description='stops the game, example: tord stop')
async


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Truth or Dare, type tord play"))
    print("YAY LET'S PLAY!")

bot.run(token)
