import os
import time
import sys

class Adventurer:
    def __init__(self, starting):
        self.name = ''
        self.inv = []
        self.location = starting
        self.game_over = False

class Item:
    def __init__(self, name, info, location):
        self.name = name
        self.info = info
        self.location = world[location]

class Room:
    def __init__(self, name, description, directions, roominv):
        self.name = name
        self.description = description
        self.directions = directions
        self.roominv = roominv

def prompt():
    print("\n=============================")
    print("Please enter a command")

    available_commands = ['quit','look']
    #Adds the available exits to the array of available commands
    available_commands.extend(world[character.location].directions.keys())
    command = input("> ").lower()
    if command not in available_commands:
        print(f"\nUnknown command, try one of {available_commands}")
        return
    if command.lower() == 'quit':
        sys.exit()
    elif command == "look":
        print(world[character.location].name + ': ' + world[character.location].description)
    elif command in world[character.location].directions.keys():
        if character.location == "starting" and command == "south":
            if "key" not in character.inv:
                print("The door is locked! You need a key")
                return
            else:
                character.game_over = True
                game_over()
        destination = world[character.location].directions[command]
        movement_handler(destination)

def movement_handler(destination):
    print("\nYou head to the " + world[destination].name + ".")
    character.location = destination

    print("Obvious Exits:", list(world[character.location].directions.keys()))

#Runs until game is complete
def main_game_loop():
    while character.game_over is False:
        prompt()

#'Main Menu' of the game, runs before the main loop
def start_game():
    question1 = ("What would you like to name your character?\n")
    message_write(question1)

    character_name = input("> ")
    character.name = character_name

    welcome = "\nWelcome " + character_name
    message_write(welcome)
    speech1 = "\nYou awake in a dark room with no memory of how you got there.\n"
    speech2 = "You must find a way out or be stuck forever.\n"
    speech3 = "You see 4 exits, North, East, West and a locked door South."
    message_write(speech1)
    message_write(speech2)
    message_write(speech3)

    time.sleep(0.5)
    print('\n')
    print("#############")
    print("#   START   #")
    print("#############")

    main_game_loop()

#Function which gives the message the writing effect in the console
def message_write(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)

def game_over():
    pass

#Creation of all the rooms
world = {
    "starting": Room("Starting Room", "You are in a dark room with nothing around", { "west": "candle", "north": "skull", "east": "safe", "south": "game over" }, []),
    "candle": Room("Candle Room", "It is cold but there are unlit candles in the corner of the room", { "east": "starting" }, []),
    "skull": Room("Skull Room", "It is muggy, a skull lays on a pile of bones in the corner", { "south": "starting" }, []),
    "safe": Room("Mystery Room", "Floor is damp and theres a weirdly specific hole in the wall", { "west": "starting", "east": "office" }, []),
    "office": Room("Office Room", "There is a desk on the far side of the room", { "west": "safe" }, [])
    }

character = Adventurer("starting")

start_game()
