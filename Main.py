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

    def pickup():
        message_write("\nWhat item would you like to pickup?")
        message_write("\nWrite 'back' to cancel")
        item = input("\n> ").lower()
        available_items = world[character.location].roominv
        if(item == "back"):
            message_write("\nYou have gone back")
            return
        while item not in world[character.location].roominv:
            if(item == "back"):
                message_write("\nYou have gone back")
                return
            message_write(f"\nItem is not valid try {available_items}")
            item = input("\n> ")
        print(f"You have picked up {items[item].name}")
        character.inv.append(item)
        world[character.location].roominv.remove(item)

    def use(item):
        while (item not in character.inv) or (item == 'back'):
            message_write("\nNot a valid item try again")
            message_write("\nWrite 'back' to cancel")
            item = input("\n> ").lower()
        if item == 'back':
            message_write("\nYou have gone back")
            return
        elif item == 'ciggarette':
            if 'lighter' in character.inv:
                message_write("\nYou smoke the ciggarette and throw it on the floor")
                character.inv.remove('ciggarette')
                return
            else:
                message_write("\nYou need something to light this")
                return


class Room:
    def __init__(self, name, description, directions, roominv):
        self.name = name
        self.description = description
        self.directions = directions
        self.roominv = roominv

def prompt():
    print("\n=============================")
    print("Please enter a command")

    available_commands = ['quit','look','pickup','inv','use']
    #Adds the available exits to the array of available commands
    available_commands.extend(world[character.location].directions.keys())
    command = input("> ").lower()
    if command not in available_commands:
        print(f"\nUnknown command, try one of {available_commands}")
        return
    #quit
    if command.lower() == 'quit':
        sys.exit()
    #look
    elif command == "look":
        print(world[character.location].name + ': ' + world[character.location].description)
    #pickup
    elif command == "pickup":
        if len(world[character.location].roominv) == 0:
            message_write("\nThere is nothing to pick up, try another room")
        else:
            Item.pickup()
    #inv
    elif command == "inv":
        print(character.inv)
    #movement
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
    #use items
    elif command == 'use':
        if len(character.inv) == 0:
            message_write("\nYour inventory is empty, try and find something to use!")
        else:
            message_write(f"\nWhat item would you like to use: {character.inv}")
            message_write("\nWrite 'back' to cancel")
            item = input("\n> ").lower()
            Item.use(item)

#changes the location of the character and describes the next location
def movement_handler(destination):
    print("\nYou head to the " + world[destination].name + ".")
    character.location = destination

    print("Obvious Exits:", list(world[character.location].directions.keys()))
    if len(world[character.location].roominv) == 0:
        print("Visible Items: None")
    else:
        print("Visible Items: ", world[character.location].roominv)

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

    message_write("\nYou awake in a dark room with no memory of how you got there.\n")
    message_write("You must find a way out or be stuck forever.\n")
    message_write("You see 4 exits, North, East, West and a locked door South.")
    print("\n")

    available_commands = ['quit','look','pickup','inv','use']
    available_commands.extend(world[character.location].directions.keys())
    print("Try: ", available_commands)

    main_game_loop()

#Function which gives the message the writing effect in the console
def message_write(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)

def game_over():
    pass

#Creation of all the rooms and items in a dictionary
world = {
    "starting": Room("Starting Room", "You are in a dark room with nothing around", { "west": "candle", "north": "skull", "east": "safe", "south": "game over" }, []),
    "candle": Room("Candle Room", "It is cold but there are unlit candles in the corner of the room", { "east": "starting" }, []),
    "skull": Room("Skull Room", "It is muggy, a skull lays on a pile of bones in the corner", { "south": "starting" }, ["skull"]),
    "safe": Room("Mystery Room", "Floor is damp and theres a weirdly specific hole in the wall", { "west": "starting", "east": "office" }, []),
    "office": Room("Office Room", "There is a desk on the far side of the room", { "west": "safe" }, ["ciggarette", "lighter"])
    }

items = {
    "ciggarette": Item("Ciggarette", "Bit dirty, but still smokable", "office"),
    "lighter": Item("Lighter", "Gas is suprisingly full", "office"),
    "skull": Item("Rounded Skull", "Has some cracks but pretty smooth", "skull")
    }

character = Adventurer("starting")

start_game()
