import os
import json

def load():
    # Read in the JSON file as it currently exists
    with open('data/annals.json', "r") as json_file:
        data = json.load(json_file)
        return data

def save( data ):
    with open('data/annals.json', 'w') as json_file:
        json.dump(data, json_file)

def find_knight(name, data):
    already_exists = False
    for knight in data['knights']:
        if knight['name'] == name:
            return knight
    return []