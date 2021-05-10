import discord
from discord.ext import commands
import random

# List used as stack to track cards in feast deck
feast_deck = []

@commands.command()
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


@commands.command()
async def draw(ctx):
    if feast_deck:
        card = feast_deck.pop()
        page = card // 9
        index = card % 9

        # Send page and index info as 1-indexed for non-programmers to understand
        await ctx.send("Drew card " + str(card) + ": page " + str(page + 1) + ", index " + str(index + 1))
    else:
        await ctx.send("Deck is empty. Reshuffle and draw again")


def setup(bot):
    # Every extension should have this function
    bot.add_command(draw)
    bot.add_command(shuffle)