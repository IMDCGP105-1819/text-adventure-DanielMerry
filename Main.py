import os
import time

#First room where player starts
def startingroom(inv):
    print("--Starting Room")
    print("Obvious Exits: 'North' 'East' 'West'")
    print("Visible Items: 'Locked Door South'")
    print("<--------------------------------------------------------------------------->")

    #commands the player can use whilst in that room, sends to a diff function which checks
    #if users input is one of these commands, or a general command
    commands = ['go north', 'north', 'go east', 'east', 'go west', 'west', 'look']
    command = selectchoice(commands)

    #defines each command and runs what the user inputs
    if(command.lower() == 'go north' or command.lower() == 'north'):
        os.system('cls')
        print("You head North\n")
        time.sleep(1)
        skullroom(inv)
    elif(command.lower() == 'go east' or command.lower() == 'east'):
        os.system('cls')
        print("You head East\n")
        time.sleep(1)
        saferoom(inv)
    elif(command.lower() == 'go west' or command.lower() == 'west'):
        os.system('cls')
        print("You head West\n")
        time.sleep(1)
        candleroom(inv)
    elif(command.lower() == 'go south' or command.lower() == 'south'):
        #checks in the key is in the inventory to open the door
        if('key' in inv):
            print("You use the key to open the door.")
            time.sleep(1)
            print("It reveals a stairway to the outside and you walk out")
            time.sleep(1)
            print("\nCongratulations. Thank you for playing")
        else:
            os.system('cls')
            print("This door is locked you cannot enter.\n")
            time.sleep(1)
            startingroom(inv)
    elif(command.lower() == 'look'):
        os.system('cls')
        print("The room is empty and dark with a cold draft.\n")
        time.sleep(1)
        startingroom(inv)
        
#room west of starting room       
def candleroom(inv):
    print("--Candle Room")
    print("Obvious Exits: 'East'")
    print("Visible Items: 'Unlit candles in the corner'")
    print("<--------------------------------------------------------------------------->")    

    commands = ['go east', 'east', 'look']
    command = selectchoice(commands)

    if(command.lower() == 'go east' or command.lower() == 'east'):
        os.system('cls')
        print("You head East\n")
        time.sleep(1)
        startingroom(inv)
    elif(command.lower() == 'look'):
        os.system('cls')
        print("This room is pitch black but you can faintly see candles in the corner of the room\n")
        time.sleep(1)
        candleroom(inv)

#room east of starting room
def saferoom(inv):
    print("--Mystery Room")
    print("Obvious Exits: 'East' 'West'")
    print("Visible Items: 'Hole in the wall'")
    print("<--------------------------------------------------------------------------->")

    commands = ['go east', 'east', 'go west', 'west', 'look']
    command = selectchoice(commands)

    if(command.lower() == 'go east' or command.lower() == 'east'):
        os.system('cls')
        print("You head East\n")
        time.sleep(1)
        deskroom(inv)
    elif(command.lower() == 'go west' or command.lower() == 'west'):
        os.system('cls')
        print("You head West\n")
        time.sleep(1)
        startingroom(inv)
    elif(command.lower() == 'look'):
        os.system('cls')
        print("The walls are covered in mould. There is a strange hole in the wall, you cant see where it leads\n")
        time.sleep(1)
        saferoom(inv)
    
#room east of saferoom
def deskroom(inv):
    print("--Office Room")
    print("Obvious Exits: 'West'")
    print("Visible Items: 'Desk'")
    print("<--------------------------------------------------------------------------->")    

    commands = ['go west', 'west', 'look']
    command = selectchoice(commands)

    if(command.lower() == 'go west' or command.lower() == 'west'):
        os.system('cls')
        print("You head West\n")
        time.sleep(1)
        saferoom(inv)
    elif(command.lower() == 'look'):
        os.system('cls')
        print("The room is tiled and has a desk on the far side of the room.")
        time.sleep(1)
        deskroom(inv)

#room north of starting room
def skullroom(inv):
    print("--Skull Room")
    print("Obvious Exits: 'South'")
    print("Visible Items: 'Circular Skull in nest of bones'")
    print("<--------------------------------------------------------------------------->")

    commands = ['go south', 'south', 'look']
    command = selectchoice(commands)

    if(command.lower() == 'go south' or command.lower() == 'south'):
        os.system('cls')
        print("You head South\n")
        time.sleep(1)
        startingroom(inv)
    elif(command.lower() == 'look'):
        os.system('cls')
        print("The room has a damp ground and a horrible smell.\nThere is a circular looking skull nested upon bones.\n")
        time.sleep(1)
        skullroom(inv)

def selectchoice(commands):
    choice = input("\n> ")
    if choice.lower() in commands:
        return choice.lower()
    elif choice.lower() == 'quit':
        exit(0)
    elif choice.lower() == 'help':
        os.system('cls')
        print("Try:", *commands, sep = ',')
        print('\n')
        time.sleep(1)
        startingroom(inv)
    else:
        print('Invalid input')
        return selectchoice(commands)

#users inventory
inv = []

#start
print("Welcome to my first ever text based game\n")
time.sleep(1)
input("Press any key to continue...")
os.system('cls')

print("You find yourself in a dark room with nothing on you.\nThere is a locked door south and 3 other exits which are open.")
print("\nIf you need help with commands type 'help'")
print("<--------------------------------------------------------------------------->")
startingroom(inv)
