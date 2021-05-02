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

personality_mirror = {
    "chaste": "lustful",
    "lustful": "chase",
    "energetic": "lazy",
    "lazy": "energetic",
    "forgiving": "vengeful",
    "vengeful": "forgiving",
    "generous": "selfish",
    "selfish": "generous",
    "honest": "deceitful",
    "deceitful": "hoenst",
    "just": "arbitrary",
    "arbitrary": "just",
    "merciful": "cruel",
    "cruel": "merciful",
    "modest": "proud",
    "proud": "modest",
    "prudent": "reckless",
    "reckless": "prudent",
    "spiritual": "worldly",
    "wordly": "spiritual",
    "temperate": "indulgent",
    "indulgent": "temperate",
    "trusting": "suspicious",
    "suspicious": "trusting"
}

statistics = [
    "siz", "dex", "str", "con", "app"
]

skills = [
    "battle", "siege", "horsemanship", "sword", "lance", "spear", "dagger", "awareness", "boating", "compose", "courtesy",
    "dancing", "faerie lore", "falconry", "fashion", "first aid", "flirting", "folklore", "gaming", "heraldry", "hunting", "intrigue", "orate", "play", "read", "recognize",
    "religion", "romance", "singing", "stewardship", "swimming", "tourney"
]

# Startup Information
@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

    # Create a new annals file if it doesn't exist
    if not os.path.isfile('data/annals.json'):
        with open('data/annals.json', 'w') as json_file:
            data = {}
            data['claims'] = {}
            data['knights'] = {}
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
async def claim(ctx, name):
    data = utility.load()

    if name in data['knights']:
        if ctx.author.name in data['claims']:
            await ctx.send("Thou hath already claimed Sir " + data['claims'][ctx.author.name])
        else:
            data['claims'][ctx.author.name] = name
            await ctx.send(ctx.author.name + " has claimed Ser " + name)
            utility.save(data)
    else:
        await ctx.send("I know not this Ser " + name)


@bot.command()
async def unclaim(ctx):
    data = utility.load()

    if ctx.author.name in data['claims']:
        await ctx.send(ctx.author.name + " hath unclaimed Ser " + data['claims'][ctx.author.name])
        del data['claims'][ctx.author.name]
        utility.save(data)
    else:
        await ctx.send("Thou has not claimed a knight")


@bot.command()
async def knight(ctx, name):
    data = utility.load()
    
    if name in data['knights']:
        await ctx.send("Sir " + name + " is already in the annals of history")
    else:
        data['knights'][name] = {}
        data['knights'][name]['personality'] = {}
        data['knights'][name]['passions'] = {}
        data['knights'][name]['statistics'] = {}
        data['knights'][name]['skills'] = {}
        data['knights'][name]['history'] = []
        utility.save(data)
        await ctx.send("Thus marks the chapter of Sir " + name + " in the annals of history")


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

    if name in data['knights']:
        data['knights'][name]['history'].append({'glory': int(glory), "reason":event})
        utility.save(data)
        await ctx.send("May the deeds of Sir " + name + " be celebrated for countless generations")
    else:
        await ctx.send("I could not find that name. Use !knight to add a new knight or check thine spelling")
    

@bot.command()
async def summarize(ctx, *argv):
    # Parse the argument list
    arg_list = []
    for arg in argv:
        arg_list += [arg]

    data = utility.load()
    
    knight = {}
    name = ""
    if len(argv) > 0:
        name = arg_list[0]
        if name in data['knights']:
            knight = data['knights'][name]
    else:
        if ctx.author.name in data['claims']:
            name = data['claims'][ctx.author.name]
            knight = data['knights'][name]

    if knight:
        # Sum all glory
        glory = 0
        for x in knight['history']:
            glory += x['glory']
        await ctx.send("Sir " + name + " is known to have accumulated " + str(glory) + " points of glory")
    else:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")



@bot.command()
async def narrate(ctx, *argv):
    # Parse the argument list
    arg_list = []
    for arg in argv:
        arg_list += [arg]

    data = utility.load()

    knight = {}
    name = ""
    if len(argv) > 0:
        name = arg_list[0]
        if name in data['knights']:
            knight = data['knights'][name]
    else:
        if ctx.author.name in data['claims']:
            name = data['claims'][ctx.author.name]
            knight = data['knights'][name]

    if knight:
        narration = "Hear ye! Hear ye! The legend of Sir " + name + "!\n"
        narration += "---------------------------------------------------------------------\n"
        glory = 0
        knight = data['knights'][name]
        for x in range(len(knight['history'])):
            narration += str(x['glory']) + " glory for " + x["reason"] + "\n"
            glory += x['glory']

        narration += "---------------------------------------------------------------------\n"
        narration += str(glory) + " glory total!"

        await ctx.send(narration)
    else:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")


@bot.command()
async def set_skill(ctx, skill, value):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]
        
        if skill in personality_mirror:
            if not skill in knight['personality']:
                knight['personality'][skill] = {'check': False, 'value': 10}
                knight['personality'][personality_mirror[skill]] = {'check': False, 'value': 10}

            knight['personality'][skill]['value'] = int(value)
            knight['personality'][personality_mirror[skill]]['value'] = 20 - int(value)
            utility.save(data)
            await ctx.send("Sir " + name + " has " + str(value) + " " + skill + " and " + str(knight['personality'][personality_mirror[skill]]['value']) + " " + personality_mirror[skill])
        elif skill in skills:
            if not skill in knight['skills']:
                knight['skills'][skill] = {'check': False, 'value': 10}

            knight['skills'][skill]['value'] = int(value)
            utility.save(data)
            await ctx.send("Sir " + name + " has " + str(value) + " " + skill)
        elif skill in statistics:
            if not skill in knight['statistics']:
                knight['statistics'][skill] = {'check': False, 'value': 10}

            knight['statistics'][skill]['value'] = int(value)
            utility.save(data)
            await ctx.send("Sir " + name + " has " + str(value) + " " + skill)
        else:
            await ctx.send(skill + " is not a valid trait, skill, or statistic")
    else:
        await ctx.send("Thou must first claim a knight")


@bot.command()
async def set_passion(ctx, passion, value):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if not passion in knight['passions']:
            knight['passions'][passion] = {'check': False, 'value': 10}

        knight['passions'][passion]['value'] = int(value)
        utility.save(data)
        await ctx.send("Sir " + name + " has " + str(value) + " " + passion)
    else:
        await ctx.send("Thou must first claim a knight")


@bot.command()
async def remove_passion(ctx, passion):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if passion in knight['passions']:
            knight['passions'].pop(passion)
            utility.save(data)
            await ctx.send("Removed " + passion + " from Sir " + name)
        else:
            ctx.send("Sir " + name + " does not have the passion " + passion)
    else:
        await ctx.send("Thou must first claim a knight")


@bot.command()
async def check(ctx, skill):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if skill in knight['personality']:
            knight['personality'][skill]['check'] = True
            utility.save(data)
            await ctx.send("Checked " + skill + " for Sir " + name)
        elif skill in knight['passions']:
            knight['passions'][skill]['check'] = True
            utility.save(data)
            await ctx.send("Checked " + skill + " for Sir " + name)
        elif skill in knight['statistics']:
            knight['statistics'][skill]['check'] = True
            utility.save(data)
            await ctx.send("Checked " + skill + " for Sir " + name)
        elif skill in knight['skills']:
            knight['skills'][skill]['check'] = True
            utility.save(data)
            await ctx.send("Checked " + skill + " for Sir " + name)
        else:
            await ctx.send("Sir " + name + " does not have " + skill)
    else:
        await ctx.send("Thou must first claim a knight")


@bot.command()
async def uncheck(ctx, skill):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if skill in knight['personality']:
            knight['personality'][skill]['check'] = False
            utility.save(data)
            await ctx.send("Unchecked " + skill + " for Sir " + name)
        elif skill in knight['passions']:
            knight['passions'][skill]['check'] = False
            utility.save(data)
            await ctx.send("Unchecked " + skill + " for Sir " + name)
        elif skill in knight['statistics']:
            knight['statistics'][skill]['check'] = False
            utility.save(data)
            await ctx.send("Unchecked " + skill + " for Sir " + name)
        elif skill in knight['skills']:
            knight['skills'][skill]['check'] = False
            utility.save(data)
            await ctx.send("Unchecked " + skill + " for Sir " + name)
        else:
            await ctx.send("Sir " + name + " does not have " + skill)
    else:
        await ctx.send("Thou must first claim a knight")


@bot.command()
async def describe(ctx, *argv):
    # Parse the argument list
    arg_list = []
    for arg in argv:
        arg_list += [arg]

    data = utility.load()

    knight = {}
    name = ""
    if len(argv) > 0:
        name = arg_list[0]
        if name in data['knights']:
            knight = data['knights'][name]
        else:
            await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")
            return
    else:
        if ctx.author.name in data['claims']:
            name = data['claims'][ctx.author.name]
            knight = data['knights'][name]
        else:
            await ctx.send("Claim a knight or specify the knight you wish to know")
            return

    if knight:
        narration = "                                  Sir " + name + ":\n"
        narration += "---------------------------------------------------------------------\n"
        narration += "                                  Personality Traits:" + "\n"
        for key, value in personality_mirror.items():
            if list(personality_mirror.keys()).index(key) % 2 == 0: # Skip every odd key in personality_mirror
                if key in knight['personality']:
                    if knight['personality'][key]['check']:
                        narration += '[x] '
                    else:
                        narration += '[ ] '

                    narration +=  str(key) + ": " + str(knight['personality'][key]['value']) + ", " + str(value) + ": " + str(knight['personality'][value]['value'])

                    if knight['personality'][value]['check']:
                        narration += ' [x]' + '\n'
                    else:
                        narration += ' [ ]' + '\n'

        narration += "---------------------------------------------------------------------\n"
        narration += "                                         Passions:" + "\n"
        for key in knight['passions']:
            if knight['passions'][key]['check']:
                narration += '[x] '
            else:
                narration += '[ ] '
            narration += str(key) + ": " + str(knight['passions'][key]['value']) + "\n"

        narration += "---------------------------------------------------------------------\n"
        narration += "                                         Statistics:" + "\n"
        for key in knight['statistics']:
            if knight['statistics'][key]['check']:
                narration += '[x] '
            else:
                narration += '[ ] '
            narration += str(key) + ": " + str(knight['statistics'][key]['value']) + "\n"

        narration += "---------------------------------------------------------------------\n"
        narration += "                                            Skills:" + "\n"
        for key in knight['skills']:
            if knight['skills'][key]['check']:
                narration += '[x] '
            else:
                narration += '[ ] '
            narration += str(key) + ": " + str(knight['skills'][key]['value']) + "\n"

        await ctx.send(narration)


@bot.command()
async def gm_skill(ctx, skill_name, difficulty, *argv):
    await ctx.send(ctx.author.display_name + utility.roll(skill_name, difficulty, *argv))


@bot.command()
async def skill(ctx, skill_name, *argv):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]
        
        if skill_name in knight['personality']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['personality'][skill_name], *argv))
        elif skill_name in knight['passions']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['passions'][skill_name], *argv))
        elif skill_name in knight['statistics']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['statistics'][skill_name], *argv))
        elif skill_name in knight['skills']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['skills'][skill_name], *argv))
        else:
            await ctx.send("Sir " + name + " does not have that skill, trait, or passion")
    else:
        await ctx.send("Thou must first claim a knight")


# Run the bot
bot.run(TOKEN)