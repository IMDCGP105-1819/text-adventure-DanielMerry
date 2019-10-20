import os
import time

#first room where user spawns
def startingroom(inv):
    print("You find yourself in a gray, dirty room. There is a cold draft.\n")
    time.sleep(1)
    print("Commands you can execute:\n>'go north'\n>'north'")

    commands = ['go north','north']
    command = selectchoice(commands)

    if(command.lower() == 'go north' or command.lower() == 'north'):
        os.system('cls')
        nextroom(inv)

#room next to the starting room, includes an item which you need to go back
def nextroom(inv):
    if('item' in inv):
        print("This room is warm :O\n")
        time.sleep(1)
        print("Commands you can execute:\n>'go south'\n>'south'")
        commands = ['go south', 'south']
    else:
        print("The door locked behind you... how will you escape :O\n")
        time.sleep(1)
        print("Commands you can execute:\n>'go south'\n>'south'\n>'take item'")
        commands = ['go south', 'south', 'take item']

    command = selectchoice(commands)

    if(command.lower() == 'go south' or command.lower() == 'south'):
        if('item' in inv):
            os.system('cls')
            startingroom(inv)
        else:
            os.system('cls')
            print("You need the item!!!\n")
            nextroom(inv)
    elif(command.lower() == 'take item'):
        inv.append('item')
        os.system('cls')
        print("You took the item!\n")
        nextroom(inv)

#goes through until the command is valid and returns the users command
def selectchoice(commands):
    choice = input("\n> ")
    if choice.lower() in commands:
        return choice.lower()
    elif choice == 'quit':
        exit(0)
    else:
        print('Invalid input')
        return selectchoice(commands)

#players inventory starts empty
inv = []

print("Starting...")
print("---------------")
startingroom(inv)
