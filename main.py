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


# Run the bot
bot.run(TOKEN)