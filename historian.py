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
    "worldly": "spiritual",
    "temperate": "indulgent",
    "indulgent": "temperate",
    "trusting": "suspicious",
    "suspicious": "trusting",
    "valorous": "cowardly"
}

statistics = [
    "siz", "dex", "str", "con", "app"
]

skills = [
    "battle", "siege", "horsemanship", "sword", "lance", "spear", "dagger", "awareness", "boating", "compose", "courtesy",
    "dancing", "faerie lore", "falconry", "fashion", "first aid", "flirting", "folklore", "gaming", "heraldry", "hunting", "intrigue", "orate", "play", "read", "recognize",
    "religion", "romance", "singing", "stewardship", "swimming", "tourney"
]

def closestSkill(skill):
    shortest_lev_distance = 1000
    closest = ""
    for x in personality_mirror:
        lev_dist = utility.levenshteinDistance(skill, x)
        if lev_dist < shortest_lev_distance:
            closest = x
            shortest_lev_distance = lev_dist
    for x in statistics:
        lev_dist = utility.levenshteinDistance(skill, x)
        if lev_dist < shortest_lev_distance:
            closest = x
            shortest_lev_distance = lev_dist
    for x in skills:
        lev_dist = utility.levenshteinDistance(skill, x)
        if lev_dist < shortest_lev_distance:
            closest = x
            shortest_lev_distance = lev_dist
    return closest


def closestPassion(passion, passion_list):
    shortest_lev_distance = 1000
    closest = ""
    for x in passion_list:
        lev_dist = utility.levenshteinDistance(passion, x)
        if lev_dist < shortest_lev_distance:
            closest = x
            shortest_lev_distance = lev_dist
    return closest


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
            narration += str(knight['history'][x]['glory']) + " glory for " + knight['history'][x]["reason"] + "\n"
            glory += knight['history'][x]['glory']

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
            await ctx.send(skill + " is not a valid trait, skill, or statistic. Did you mean " + '\'' + closestSkill(skill) + "\'?")
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
            await ctx.send("Sir " + name + " does not have " + skill + ". Did you mean " + '\'' + closestSkill(skill) + "\'?")
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
            await ctx.send("Sir " + name + " does not have " + skill + ". Did you mean" + '\'' + closestSkill(skill) + "\'?")
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
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['personality'][skill_name]['value'], *argv))
        elif skill_name in knight['passions']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['passions'][skill_name]['value'], *argv))
        elif skill_name in knight['statistics']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['statistics'][skill_name]['value'], *argv))
        elif skill_name in knight['skills']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['skills'][skill_name]['value'], *argv))
        else:
            closest_passion = closestPassion(skill_name, knight['passions'])
            closest_skill = closestSkill(skill_name)
            message = ": Sir " + name + " does not have that skill, trait, or passion. Did you mean "
            if utility.levenshteinDistance(closest_passion, skill_name) < utility.levenshteinDistance(closest_skill, skill_name):
                message += '\'' + closest_passion + "\'?"
            else:
                message += '\'' + closest_skill + "\'?"
            await ctx.send(ctx.author.display_name + message)
    else:
        await ctx.send("Thou must first claim a knight")

feast_deck = []

@bot.command()
async def shuffle(ctx):
    # Create a list of numbers from 0 to the last card in the deck
    NUM_CARDS = 155
    card_list = [num for num in range(0, NUM_CARDS)]

    # Randomly pick cards and push them onto the feast deck
    while (card_list):
        rand_idx = random.randint(0, len(card_list)-1)
        feast_deck.append(card_list[rand_idx])
        card_list.remove(card_list[rand_idx])

    await ctx.send("Shuffled the feast deck")


@bot.command()
async def draw(ctx):
    if feast_deck:
        card = feast_deck.pop()
        page = card // 9
        index = card % 9

        # Send page and index info as 1-indexed for non-programmers to understand
        await ctx.send("Drew card " + str(card) + ": page " + str(page + 1) + ", index " + str(index + 1))
    else:
        await ctx.send("Deck is empty. Reshuffle and draw again")


@bot.command()
async def roll(ctx, *argv):
    # Take argument list and concatentate as a single string
    argument = ""
    for arg in argv:
        argument += arg

    # Split at all '+' and then split at all '-'
    plus_split = argument.split('+')
    arg_list = []
    for i in plus_split:
        temp = i.split('-')
        if len(temp) > 1:
            arg_list.append(temp[0])
            for k in temp[1:]:
                arg_list.append(str(0 - int(k)))
        else:
            arg_list.append(temp[0])

    rolls = []
    bonus = 0
    total = 0

    # Parse each argument and roll dice
    for it in arg_list:
        try:
            # Straight conversions to integer mean the argument is a bonus
            bonus += int(it)
        except ValueError:
            split = it.split('d')
            if (len(split) == 2):
                # Compute the roll
                num_rolls = 1
                if split[0]:
                    num_rolls = int(split[0])

                for i in range(num_rolls):
                    roll_val = random.randint(0, int(split[1]))
                    rolls.append(roll_val)
                    total += roll_val
            else:
                await ctx.send("I could not understand that roll")
                return

    message = ctx.author.name + " Roll: " + str(total + bonus) + "\n     rolls: ["
    for i in rolls[:-1]:
        message += str(i) + ", "
    if rolls:
        message += str(rolls[-1])
    message += "] "

    if bonus != 0:
        message += "bonus " + str(bonus)

    await ctx.send(message)


# Run the bot
bot.run(TOKEN)