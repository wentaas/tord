from random import sample, choice
from asyncio import TimeoutError
import discord

bot = discord.Client()
token = "not set"
games = {}

with open('truth_questions.txt', 'r', encoding='utf-8') as f:
    truth_questions = f.read().splitlines()
with open('dare_questions.txt', 'r', encoding='utf-8') as f:
    dare_questions = f.read().splitlines()


async def roll(c, a):
    if a.id in games:
        choices = sample(games[a.id], 2)
        await c.send(f"{choices[0]} asks {choices[1]}")


async def game(c, a, rem=False):
        await c.send("YAY!! mention everyone you want to add")
        try:
            msg = await bot.wait_for('message', timeout=120)
            if msg.author == a:
                if len(msg.mentions) > 0:
                    added = []
                    not_added = []
                    players = []
                    mentions = msg.mentions
                    if a.id in games:
                        players = games[a.id]
                    if rem:
                        for name in mentions:
                            if name.mention in players:
                                added.append(name.mention)
                                players.pop(name.mention)
                            else:
                                not_added.append(name.mention)
                        await c.send(f"{added} removed from the game, see you again!!")
                        if not_added:
                            await c.send(f"{not_added} weren't in the game anyway")
                        games[a.id] = players
                    else:
                        for name in mentions:
                            if name.mention not in players:
                                added.append(name.mention)
                            else:
                                not_added.append(name.mention)
                        if a.mention in mentions:
                            players.append(a.mention)
                        await c.send(f"{added} in the game")
                        if not_added:
                            await c.send(f"{not_added} were already in the game tho")
                        if a.mention not in players:
                            players.append(a.mention)
                        games[a.id] = players
                    await c.send("just type ``roll`` after answering and ``tord stop`` to end the game\nto add players type ``tord add`` and ``tord remove`` to you can also use ``tord stuck truth`` or"
                                 "``tord stuck dare`` if you want a question recommendation\nok enough talking **LET'S GOOO!**")
                else:
                    await c.send(f"but you didn't mention anyone, are you confused? you just mention them\nuse the command again please", delete_after=10)
        except TimeoutError:
            await c.send("you didn't tag anyone, don't you wanna play :(", delete_after=10)


@bot.event
async def on_message(m):
    t = m.content.lower()
    a = m.author
    c = m.channel
    if t.startswith('tord play'):
        if a.id not in games:
            await game(c, a)
        else:
            await c.send(f"you already have a game, type ``tord stop`` to end it", delete_after=10)
    if t.startswith('tord stop', 'tord add', 'tord remove'):
        if a.id in games:
            if t.startswith('tord stop'):
                games.pop(a.id)
                await c.send("i hope it was a good game, bye for now!!")
            elif t.startswith('tord add'):
                await game(c, a)
            elif t.startswith('tord remove'):
                await game(a, c, True)
        else:
            await c.send("you don't have a game tho, type ``tord play`` to start one")
    elif t.startswith('tord truth'):
        await c.send(choice(truth_questions))
    elif t.startswith('tord dare'):
        await c.send(choice(dare_questions))
    elif t == 'roll':
        await roll(c, a)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Truth or Dare, type tord play"))
    print("YAY LET'S PLAY!")

bot.run(token)
