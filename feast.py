import discord
from discord.ext import commands
import random

# List used as stack to track cards in feast deck
feast_deck = []

"""
Name: shuffle
Summary: Shuffles the feast deck. Any previously drawn cards are re-added to the deck.
"""
@commands.command()
async def shuffle(ctx):
    # Create a list of numbers from 0 to the last card in the deck
    NUM_CARDS = 154
    card_list = [num for num in range(1, NUM_CARDS+1)]

    # Randomly pick cards and push them onto the feast deck
    while (card_list):
        rand_idx = random.randint(0, len(card_list)-1)
        feast_deck.append(card_list[rand_idx])
        card_list.remove(card_list[rand_idx])

    await ctx.send("Shuffled the feast deck")


"""
Name: draw
Summary: Draws a card from the feast deck. The feast deck must not be empty and must have been shuffled at least once
"""
@commands.command()
async def draw(ctx):
    if feast_deck:
        card = feast_deck.pop()
        card_name = "feast_cards/slice" + str(card) + ".png"
        await ctx.send(file=discord.File(card_name))
    else:
        await ctx.send("Deck is empty. Reshuffle and draw again")


# Allows this file's bot commands to be loaded in to a separate file
# Every extension should have this function
def setup(bot):
    bot.add_command(draw)
    bot.add_command(shuffle)