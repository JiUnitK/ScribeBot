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

# Load extensions
bot.load_extension("feast")
bot.load_extension("historian")


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


"""
Name: roll
Summary: Performs a generic dice roll

Note: Format follows any number of provided XdY, dY, or integer values

Examples: !roll d20+5
          !roll d20 + 5
          !roll 3d12 + d5 + 5
          !roll 3d6 + 1d6 - 3 + 4
          !roll 3d6+1d6-3+4
"""
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
                    roll_val = random.randint(1, int(split[1]))
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