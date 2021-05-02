import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import json

import utility

# Load the bot token from the .env file in this directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot
bot = commands.Bot(command_prefix='!')

# Startup Information
@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

    # Create a new annals file if it doesn't exist
    if not os.path.isfile('data/annals.json'):
        with open('data/annals.json', 'w') as json_file:
            data = {}
            data['knights'] = []
            json.dump(data, json_file)


@bot.command()
async def swoon(ctx):
    players = ["Sir Pant", "Sir Griffyth", "Sir Percival", "Sir Bylandt"]
    random_compliments = [
        "{player} is so handsome!",
        "Look at {player}'s massive arms!",
        "{player} is more imposing than the rumors say...",
        "Mayhap if I were so fortunate, I would lock eyes with {player}.",
        "Make way for {player}!"
    ]

    random_player = players[random.randint(0, len(players) - 1)]
    random_compliment = random_compliments[random.randint(0, len(random_compliments) - 1)]

    await ctx.send(random_compliment.format(player=random_player))

@bot.command()
async def insult(ctx, name):
    random_shame = [
        "Thou callest that a glory score Ser {player}? How pitiable!",
        "Lo! Doth the earth quake? Or is Ser {player}'s mother taking a walk?",
        "Speaking of Ser {player}, doth knowest what they say about those with low glory?"
    ]
    random_insult = random_shame[random.randint(0, len(random_shame) - 1)]
    await ctx.send(random_insult.format(player=name))


@bot.command()
async def knight(ctx, name):
    data = utility.load()
    knight = utility.find_knight(name, data)
    if knight:
        data['knights'].append({
            'name': name,
            'history': [],
            'glory': [],
        })
        utility.save(data)

        await ctx.send("Thus marks the chapter of Sir " + name + " in the annals of history")
    else:
        await ctx.send("Sir " + name + " is already in the annals of history")


@bot.command()
async def glorify(ctx, *argv):
    # From user perspective, first name should be name, then amount of glory, and then the last element should be event name
    # argv is used because users sometimes add extra characters they shouldn't

    # Parse the argument list
    arg_list = []
    for arg in argv:
        arg_list += [arg]

    name = arg_list[0]
    glory = arg_list[1]
    event = arg_list[-1]

    data = utility.load()
    
    # Check for knight name
    knight = utility.find_knight(name, data)
    if knight:
        knight['history'].append(event)
        knight['glory'].append(int(glory))
        utility.save(data)
        await ctx.send("May the deeds of Sir " + name + " be celebrated for countless generations")
    else:
        await ctx.send("I could not find that name. Use !knight to add a new knight or check thine spelling")
    

@bot.command()
async def summarize(ctx, name):
    data = utility.load()
    
    knight = utility.find_knight(name, data)
    if knight:
        # Sum all glory
        glory = 0
        for x in knight['glory']:
            glory += x
        await ctx.send("Sir " + name + " is known to have accumulated " + str(glory) + " points of glory")
    else:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")


@bot.command()
async def skill(ctx, skill_name, difficulty, *argv):
    bonus_list = []
    for arg in argv:
        bonus_list += [arg]

    difficulty = int(difficulty)

    bonus = 0
    for x in bonus_list[0:]:
        bonus += int(x)

    difficulty += bonus

    crit_range = [difficulty, difficulty]
    if difficulty > 20:
        crit_range[1] = 20
        crit_range[0] = 20 - (difficulty - 20)

    roll = random.randint(1, 20)
    output_str = skill_name
    if roll == 1:
        output_str += " -> fumble\n   (rolled 1)"
    elif roll >= crit_range[0] and roll <= crit_range[1]:
        output_str += " -> CRIT!\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    elif roll < difficulty:
        output_str += " -> success!\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    else:
        output_str += " -> fail\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    
    await ctx.send(output_str)

@bot.command()
async def narrate(ctx, name):
    data = utility.load()

    knight = utility.find_knight(name, data)
    if knight:
        narration = "Hear ye! Hear ye! The legend of Sir " + name + "!\n"
        narration += "---------------------------------------------------------------------\n"
        glory = 0
        for x in range(len(knight['glory'])):
            narration += str(knight['glory'][x]) + " glory for " + knight['history'][x] + "\n"
            glory += knight['glory'][x]

        narration += "---------------------------------------------------------------------\n"
        narration += str(glory) + " glory total!"

        await ctx.send(narration)
    else:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")

# Run the bot
bot.run(TOKEN)