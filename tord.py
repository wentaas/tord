import random
import asyncio
import discord

bot = discord.Client( )
token = "NzA4Nzc3OTUyOTc1OTEzMDEz.XrcTNg.vwRzxUISzp-UFyi1nwO7q-3zMb0"
games = {}

with open('truth_questions.txt', 'r', encoding='utf-8') as f:
    truth_questions = f.read().splitlines()
with open('dare_questions.txt', 'r') as f:
    dare_questions = f.read().splitlines()


@bot.event
async def on_message(m):
    t = m.content
    a = m.author
    c = m.channel
    if t.startswith('tord play'):
        mention = a.mention
        if a.id not in games:
            await c.send("YAY mention everyone that's gonna play")
            try:
                msg = await bot.wait_for('message', timeout=60)
                if msg.author == a:
                    if len(msg.mentions) > 0:
                        players = msg.mentions
                        if mention not in players:
                            players.append(a.mention)
                        games[a.id] = players
                        await c.send("just type ``roll`` after answering and ``tord stop`` to end the game\nyou can also use ``tord stuck truth`` or ``tord stuck dare`` if you want a question recommendation"
                                     "\nok enough talking **LET'S GOOO!**")
                        await c.send(f"{random.choice(players)} asks {random.choice(players)}")
                    else:
                        await c.send(f"but you didn't mention anyone, are you confused? you just mention them\nuse the command again please", delete_after=60)
            except asyncio.TimeoutError:
                await c.send("you didn't tag anyone, don't you wanna play :(", delete_after=60)
        else:
            await c.send(f"you already have a game, type ``tord stop`` to end it", delete_after=60)
    elif t.startswith('tord stop'):
        if a.id in games:
            games.pop(a.id)
            await c.send("i hope it was a good game, bye for now!!")
        else:
            await c.send("you don't have a game anyway, type ``tord play`` to start one")
    elif t.startswith('tord stuck'):
        if t.startswith('tord stuck truth'):
            await c.send(random.choice(truth_questions))
        elif t.startswith('tord stuck dare'):
            await c.send(random.choice(dare_questions))
        else:
            await c.send("it's either ``tord stuck truth`` or ``tord stuck dare`` tho")
    elif t == 'roll':
        id = a.id
        if id in games:
            players = games[id]
            await c.send(f"{random.choice(players)} asks {random.choice(players)}")
        else:
            await c.send("you don't have a game yet, type ``tord play`` to start one")

bot.run(token)
