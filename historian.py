import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import json

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
async def knight(ctx, name):
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)

    # Check for knight name
    already_exists = False
    for knight in data['knights']:
        if knight['name'] == name:
            await ctx.send("Sir " + name + " is already in the annals of history")
            already_exists = True
    
    # Add the new knight
    if not already_exists:
        data['knights'].append({
            'name': name,
            'history': [],
            'glory': [],
        })

        with open('data/annals.json', 'w') as json_file:
            json.dump(data, json_file)

        await ctx.send("Thus marks the chapter of Sir " + name + " in the annals of history")


@bot.command()
async def glorify(ctx, name, glory, event):
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)
    
    # Check for knight name
    for knight in data['knights']:
        if knight['name'] == name:
            knight_exists = True
            knight['history'].append(event)
            knight['glory'].append(int(glory))
            await ctx.send("May the deeds of Sir " + name + " be celebrated for countless generations")
    
    with open('data/annals.json', 'w') as json_file:
        json.dump(data, json_file)
    

@bot.command()
async def summarize(ctx, name):
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)

    # Search for knight
    knight_exists = False
    for knight in data['knights']:
        if knight['name'] == name:
            target_knight = knight
            knight_exists = True
    
    if not knight_exists:
        await ctx.send("The annals of history do not contain the names of every lowborn peasant to walk the earth")
    else:
        # Sum all glory
        glory = 0
        for x in target_knight['glory']:
            glory += x
        await ctx.send("Sir " + name + " is known to have accumulated " + str(glory) + " points of glory")

# Run the bot
bot.run(TOKEN)