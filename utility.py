import os
import json
import random

def load():
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)
        return data

def save( data ):
    with open('data/annals.json', 'w') as json_file:
        json.dump(data, json_file)

def roll( skill_name, difficulty, *argv ):
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
    output_str = " rolled " + skill_name
    if roll == 1:
        output_str += " -> fumble\n   (rolled 1)"
    elif roll >= crit_range[0] and roll <= crit_range[1]:
        output_str += " -> CRIT!\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    elif roll < difficulty:
        output_str += " -> success!\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    else:
        output_str += " -> fail\n   (rolled " + str(roll) + ", DC " + str(difficulty) + ", " + "crit range: " + str(crit_range[0]) + " to " + str(crit_range[1]) + ")"
    
    return output_str