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


# Command
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
async def addknight(ctx, name):
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)

    # Check for knight name
    already_exists = False
    for knight in data['knights']:
        if knight['name'] == name:
            await ctx.send(name + " is already in the annals of history")
            already_exists = True
    
    # Add the new knight
    if not already_exists:
        data['knights'].append({
            'name': name,
            'history': []
        })
        with open('data/annals.json', 'w') as json_file:
            json.dump(data, json_file)

# Run the bot
bot.run(TOKEN)