import discord
from discord.ext import commands
import json
import utility
import random
import re

# Dictionary of personality traits and their mirror traits
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

# List of character statistics
statistics = [
    "siz", "dex", "str", "con", "app"
]

# List of character skills
skills = [
    "battle", "siege", "horsemanship", "sword", "lance", "spear", "dagger", "awareness", "boating", "compose", "courtesy",
    "dancing", "faerie lore", "falconry", "fashion", "first aid", "flirting", "folklore", "gaming", "heraldry", "hunting", "intrigue", "orate", "play", "read", "recognize",
    "religion", "romance", "singing", "stewardship", "swimming", "tourney"
]

"""
Name: closestSkill
Summary: Returns the name of the personality trait, skill, or statistic that most closely matches the input string 'skill'
"""
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


"""
Name: closestPassion
Summary: Returns the name of the passion that most closely matches the input string 'skill'
"""
def closestPassion(passion, passion_list):
    shortest_lev_distance = 1000
    closest = ""
    for x in passion_list:
        lev_dist = utility.levenshteinDistance(passion, x)
        if lev_dist < shortest_lev_distance:
            closest = x
            shortest_lev_distance = lev_dist
    return closest


"""
Name: claim
Summary: Allows a Discord user to specify which knight character to modify or use for rolls
"""
@commands.command()
async def claim(ctx, name):
    data = utility.load()

    if name in data['knights']:
        if ctx.author.name in data['claims']:
            await ctx.send("Thou hath already claimed Sir " + data['claims'][ctx.author.name])
        else:
            data['claims'][ctx.author.name] = name
            await ctx.send(ctx.author.name + " has claimed Sir " + name)
            utility.save(data)
    else:
        await ctx.send("I know not this Sir " + name)


"""
Name: unclaim
Summary: Allows a Discord user to release control of a knight character
"""
@commands.command()
async def unclaim(ctx):
    data = utility.load()

    if ctx.author.name in data['claims']:
        await ctx.send(ctx.author.name + " hath unclaimed Sir " + data['claims'][ctx.author.name])
        del data['claims'][ctx.author.name]
        utility.save(data)
    else:
        await ctx.send("Thou has not claimed a knight")


"""
Name: knight
Summary: Creates a new knight character with the given 'name'
"""
@commands.command()
async def knight(ctx, name):
    data = utility.load()
    
    if name in data['knights']:
        await ctx.send("Sir " + name + " is already in the annals of history")
    else:
        data['knights'][name] = {}
        data['knights'][name]['personality'] = {
            'chaste': {'check': False, 'value': 10},
            'lustful': {'check': False, 'value': 10},
            'energetic': {'check': False, 'value': 10},
            'lazy': {'check': False, 'value': 10},
            'forgiving': {'check': False, 'value': 10},
            'vengeful': {'check': False, 'value': 10},
            'generous': {'check': False, 'value': 10},
            'selfish': {'check': False, 'value': 10},
            'honest': {'check': False, 'value': 10},
            'deceitful': {'check': False, 'value': 10},
            'just': {'check': False, 'value': 10},
            'arbitrary': {'check': False, 'value': 10},
            'merciful': {'check': False, 'value': 10},
            'cruel': {'check': False, 'value': 10},
            'modest': {'check': False, 'value': 10},
            'proud': {'check': False, 'value': 10},
            'prudent': {'check': False, 'value': 10},
            'reckless': {'check': False, 'value': 10},
            'spiritual': {'check': False, 'value': 10},
            'worldly': {'check': False, 'value': 10},
            'temperate': {'check': False, 'value': 10},
            'indulgent': {'check': False, 'value': 10},
            'trusting': {'check': False, 'value': 10},
            'suspicious': {'check': False, 'value': 10},
            'valorous': {'check': False, 'value': 10},
            'cowardly': {'check': False, 'value': 10},
        }
        data['knights'][name]['passions'] = {
            'fealty(lord)': {'check': False, 'value': 15},
            'love(family)': {'check': False, 'value': 15},
            'hospitality': {'check': False, 'value': 15},
            'honor': {'check': False, 'value': 15}
        }
        data['knights'][name]['statistics'] = {
            'siz': {'check': False, 'value': 10},
            'dex': {'check': False, 'value': 10},
            'str': {'check': False, 'value': 10},
            'con': {'check': False, 'value': 10},
            'app': {'check': False, 'value': 10}
        }
        data['knights'][name]['skills'] = {
            "battle": {'check': False, 'value': 10},
            "horsemanship": {'check': False, 'value': 10},
            "sword": {'check': False, 'value': 10},
            "lance": {'check': False, 'value': 10},
            "spear": {'check': False, 'value': 6},
            "dagger": {'check': False, 'value': 5},
            "awareness": {'check': False, 'value': 5},
            "boating": {'check': False, 'value': 1},
            "compose": {'check': False, 'value': 1},
            "courtesy": {'check': False, 'value': 3},
            "dancing": {'check': False, 'value': 2},
            "faerie lore": {'check': False, 'value': 1},
            "falconry": {'check': False, 'value': 3},
            "first aid": {'check': False, 'value': 10},
            "flirting": {'check': False, 'value': 3},
            "folklore": {'check': False, 'value': 2},
            "gaming": {'check': False, 'value': 3},
            "heraldry": {'check': False, 'value': 3},
            "hunting": {'check': False, 'value': 2},
            "intrigue": {'check': False, 'value': 3},
            "orate": {'check': False, 'value': 3},
            "play": {'check': False, 'value': 3},
            "read": {'check': False, 'value': 0},
            "recognize": {'check': False, 'value': 3},
            "religion": {'check': False, 'value': 2},
            "romance": {'check': False, 'value': 2},
            "singing": {'check': False, 'value': 2},
            "stewardship": {'check': False, 'value': 2},
            "swimming": {'check': False, 'value': 2},
            "tourney": {'check': False, 'value': 2},
        }
        data['knights'][name]['history'] = []
        data['knights'][name]['notes'] = {}
        utility.save(data)
        await ctx.send("Thus marks the chapter of Sir " + name + " in the annals of history")


"""
Name: claim
Summary: Adds a new entry to a knight's history with a particular glory value and summary of the event

Note: From user perspective, first name should be name, then amount of glory, and then the last element should be event name.
      argv is used because users sometimes add extra characters they shouldn't
"""
@commands.command()
async def glorify(ctx, *argv):
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
    

"""
Name: summarize
Summary: Sums up the glory score of a given knight.

Note: If no name is provided, the summary is of the user's currently claimed knight.
"""
@commands.command()
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


"""
Name: narrate
Summary: Prints full history of a given knight and a glory score sum

Note: If no name is provided, the summary is of the user's currently claimed knight.
"""
@commands.command()
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
            # Only print the last 10 items due to discord bot post character limit of 2000 characters
            if (x > len(knight['history']) - 20):
                narration += str(knight['history'][x]['glory']) + " glory for " + knight['history'][x]["reason"] + "\n"
            glory += knight['history'][x]['glory']

        narration += "---------------------------------------------------------------------\n"
        narration += str(glory) + " glory total!"

        await ctx.send(narration)
    else:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")


"""
Name: set
Summary: Sets a skill, personality trait, passion, or statistic to a target value for the currently claimed knight. 
         For personality trait, the opposing trait is reducing so that that sum of the trait with its mirror trait is 20
"""
@commands.command()
async def set(ctx, skill, value):
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
        elif skill in knight['passions']:
            knight['passions'][skill]['value'] = int(value)
            utility.save(data)
            await ctx.send("Sir " + name + " has " + str(value) + " " + skill)
        else:
            await ctx.send(skill + " is not a valid trait, skill, passion, or statistic. Did you mean " + '\'' + closestSkill(skill) + "\'?")
    else:
        await ctx.send("Thou must first claim a knight")


"""
Name: add_passion
Summary: Sets a passion for the currently claimed knight to the target value. If the passion does not already exist, a new passion is created.
"""
@commands.command()
async def add_passion(ctx, passion, value):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if not passion in knight['passions']:
            knight['passions'][passion] = {'check': False, 'value': int(value)}
        else:
            knight['passions'][passion]['value'] = int(value)

        utility.save(data)
        await ctx.send("Sir " + name + " has " + str(value) + " " + passion)
    else:
        await ctx.send("Thou must first claim a knight")

"""
Name: note
Summary: Sets a note for the currently claimed knight.
"""
@commands.command()
async def note(ctx, note, value):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]
        if not note in knight['notes']:
            knight['notes'][note] = str(value)
        else:
            knight['notes'][note] = str(value)

        utility.save(data)
        await ctx.send("Note added for Sir " + name + " - " + str(note) + ": " + str(value))
    else:
        await ctx.send("Thou must first claim a knight")

"""
Name: remove_note
Summary: Removes a note from the list of notes for the currently claimed knight
"""
@commands.command()
async def remove_note(ctx, note):
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        if note in knight['notes']:
            knight['notes'].pop(note)
            utility.save(data)
            await ctx.send("Removed note " + str(note) + " from Sir " + name)
        else:
            ctx.send("Sir " + name + " does not have that note")
    else:
        await ctx.send("Thou must first claim a knight")

"""
Name: read_notes
Summary: Reads out the notes for the currently claimed knight or a specified knight
"""
@commands.command()
async def read_notes(ctx, *argv):
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
        narration = "                                  Sir " + name + "'s Notes:\n"
        narration += "---------------------------------------------------------------------\n"
        for key in knight['notes']:
            narration += str(key) + ": " + str(knight['notes'][key]) + "\n"
        await ctx.send(narration)

"""
Name: remove_passion
Summary: Removes a passion from the list of passions for the currently claimed knight
"""
@commands.command()
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


"""
Name: check
Summary: Adds a check to the named skill, personality trait, stat, or passion for the currently claimed knight
"""
@commands.command()
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


"""
Name: uncheck
Summary: Removes a check to the named skill, personality trait, stat, or passion for the currently claimed knight
"""
@commands.command()
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


"""
Name: describe
Summary: Prints a character sheet of traits, skills, stats, and passions for the currently claimed knight or a target knight if
         a name is provided.
"""
@commands.command()
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
        narration += "                                          Derived Stats:" + "\n"
        siz = knight['statistics']['siz']['value']
        dex = knight['statistics']['dex']['value']
        strength = knight['statistics']['str']['value']
        con = knight['statistics']['con']['value']
        app = knight['statistics']['app']['value']

        narration += "Damage: " + str(round((strength + siz) / 6)) + "d6\n"
        narration += "Healing rate: " + str(round((strength + con) / 10)) + "\n"
        narration += "Move rate: " + str(round((strength + dex) / 10)) + "\n"
        narration += "Total hit points: " + str(siz + con) + "\n"
        narration += "Unconscious: " + str(round((siz + con) / 4))  + "\n"

        narration += "---------------------------------------------------------------------\n"
        narration += "                                            Skills:" + "\n"
        for key in knight['skills']:
            if knight['skills'][key]['check']:
                narration += '[x] '
            else:
                narration += '[ ] '
            narration += str(key) + ": " + str(knight['skills'][key]['value']) + "\n"
        await ctx.send(narration)


"""
Name: gm_roll
Summary: Performs a generic skill roll

Note: The parameters are a string name for the skill, the DC value, and any number of bonuses
"""
@commands.command()
async def gm_roll(ctx, skill_name, difficulty, *argv):
    await ctx.send(ctx.author.display_name + utility.roll(skill_name, difficulty, *argv))


"""
Name: roll
Summary: Performs a generic dice roll. Otherwise, performs a specific skill check.

Note: Format for generic roll follows any number of provided XdY, dY, or integer values

Examples: !roll d20+5
          !roll d20 + 5
          !roll 3d12 + d5 + 5
          !roll 3d6 + 1d6 - 3 + 4
          !roll 3d6+1d6-3+4

Note: Format for skill command is the skill name followed by any number of bonuses

Examples: !roll awareness 20
          !roll chaste
          !roll hunting -2
"""
@commands.command()
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
    message = ""

    # Load the knight claimed by the user, if any exists
    data = utility.load()
    if ctx.author.name in data['claims']:
        name = data['claims'][ctx.author.name]
        knight = data['knights'][name]

        # If the first argument matches the name of a skill, trait, etc. roll for that trait
        skill_name = argv[0]
        if skill_name in knight['personality']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['personality'][skill_name]['value'], *argv[1:]))
            return
        elif skill_name in knight['passions']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['passions'][skill_name]['value'], *argv[1:]))
            return
        elif skill_name in knight['statistics']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['statistics'][skill_name]['value'], *argv[1:]))
            return
        elif skill_name in knight['skills']:
            await ctx.send(ctx.author.display_name + utility.roll(skill_name, knight['skills'][skill_name]['value'], *argv[1:]))
            return
    
    # This is a generic roll. Parse each argument and roll dice
    for it in arg_list:
        try:
            # Straight conversions to integer mean the argument is a bonus
            bonus += int(it)
        except ValueError:
            # Check for rolls like d20 or 2d20
            match_obj1 = re.match(r"\d[d]\d", it)
            match_obj2 = re.match(r"[d]\d", it)
            if match_obj1:
                split = it.split('d')
                num_rolls = int(split[0])
                for i in range(num_rolls):
                    roll_val = random.randint(1, int(split[1]))
                    rolls.append(roll_val)
                    total += roll_val
            elif match_obj2:
                roll_val = random.randint(1, int(it[1:]))
                rolls.append(roll_val)
                total += roll_val
            else:
                await ctx.send("Skills with spaces should be enclosed with parentheses and claim a knight if you haven't.")
                return

    # Format the roll result
    message = ctx.author.name + " Roll: " + str(total + bonus) + "\n     rolls: ["
    for i in rolls[:-1]:
        message += str(i) + ", "
    if rolls:
        message += str(rolls[-1])
    message += "] "

    if bonus != 0:
        message += "bonus " + str(bonus)

    await ctx.send(message)


# Allows this file's bot commands to be loaded in to a separate file
# Every extension should have this function
def setup(bot):
    bot.add_command(claim)
    bot.add_command(unclaim)
    bot.add_command(knight)
    bot.add_command(glorify)
    bot.add_command(summarize)
    bot.add_command(narrate)
    bot.add_command(set)
    bot.add_command(note)
    bot.add_command(remove_note)
    bot.add_command(read_notes)
    bot.add_command(add_passion)
    bot.add_command(remove_passion)
    bot.add_command(check)
    bot.add_command(uncheck)
    bot.add_command(describe)
    bot.add_command(gm_roll)
    bot.add_command(roll)