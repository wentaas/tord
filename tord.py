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


async def roll(c, players):
    choices = sample(players, 2)
    await c.send(f"{choices[0]} asks {choices[1]}")


@bot.event
async def on_message(m):
    t = m.content
    a = m.author
    c = m.channel
    if t.startswith('tord play'):
        if a.id not in games:
            await c.send("YAY!! mention everyone that's gonna play")
            try:
                msg = await bot.wait_for('message', timeout=120)
                if msg.author == a:
                    if len(msg.mentions) > 0:
                        players = []
                        for name in msg.mentions:
                            if name.mention not in players:
                                players.append(name.mention)
                        if a.mention not in players:
                            players.append(a.mention)
                        games[a.id] = players
                        await c.send("just type ``roll`` after answering and ``tord stop`` to end the game\nyou can also use ``tord stuck truth`` or ``tord stuck dare`` if you want a question recommendation"
                                     "\nok enough talking **LET'S GOOO!**")
                        await roll(c, players)
                    else:
                        await c.send(f"but you didn't mention anyone, are you confused? you just mention them\nuse the command again please", delete_after=10)
            except TimeoutError:
                await c.send("you didn't tag anyone, don't you wanna play :(", delete_after=10)
        else:
            await c.send(f"you already have a game, type ``tord stop`` to end it", delete_after=10)
    elif t.startswith('tord stop'):
        if a.id in games:
            games.pop(a.id)
            await c.send("i hope it was a good game, bye for now!!")
        else:
            await c.send("you don't have a game anyway, type ``tord play`` to start one")
    elif t.startswith('tord truth'):
        await c.send(choice(truth_questions))
    elif t.startswith('tord dare'):
        await c.send(choice(dare_questions))
    elif t == 'roll':
        id = a.id
        if id in games:
            players = games[id]
            await roll(c, players)
        else:
            await c.send("you don't have a game yet, type ``tord play`` to start one", delete_after=10)


@bot.event
async def on_ready():
    print("YAY LET'S PLAY!")

bot.run(token)
