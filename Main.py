import json

class Character(object):
    def __init__(self, name, location, inv):
        self.name = name
        self.location = location
        self.inv = inv
        self.escaped = False

    def drop(self, item):
        self.inv.remove(item)
        self.location.inv.append(item)
        print(f"You have dropped: {item}")

    def pickup(self, item):
        self.inv.append(item)
        self.location.inv.remove(item)
        print(f"You have picked up: {item}")

    def use(self, item):
        if item == 'key':
            if self.location == world['starting']:
                print("\nYou have used the key to unlock the door")
                self.inv.remove('key')
                starting.unlock()
                world['starting'].description = 'The door is now open south'
            else:
                print("\nYou cannot use that here.")

        if item == 'lighter':
            if self.location == world['candle']:
                print("\nYou use the lighter to light the candles, there is blood on the walls")
                world['candle'].description = 'The room is lit up and there is blood on the walls'
            else:
                print("\nYou cannot use that here.")

        if item == 'skull':
            if self.location == world['cold']:
                print("\nYou place the skull in the hole in the wall, a key falls onto the floor!")
                self.inv.remove('skull')
                self.location.inv.append('key')
            else:
                print("\nYou cannot use that here.")

        if item == 'ciggarette':
            if 'lighter' in self.inv:
                print("You smoke the ciggarette and throw the filter on the floor.")
                self.inv.remove('ciggarette')
            else:
                print("You need something to light this")

        if item == 'bone':
            print('\nYou cannot use that here')

    def getInventory(self):
        if len(self.inv) == 0:
            return 'You have nothing in your inventory'
        else:
            return ', '.join(self.inv)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
    
class Room(object):
    def __init__(self, name, description, inv, exits):
        self.name = name
        self.description = description
        self.inv = inv
        self.exits = exits
        
        if self.name == 'starting':
            self.locked = True

    def look(self):
        return self.description

    def __str__(self):
        return self.name + ' room'

    def __repr__(self):
        return str(self)

    def unlock(self):
        self.locked = False

    def deskItems(self):
        if len(self.inv) == 0:
            return 'Empty'
        else:
            return ', '.join(self.inv)

class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def look(self):
        return self.description

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

#Rooms
starting = Room('starting', 'There is a locked door south', [], {'w': 'candle', 'n': 'skull', 'e': 'cold'})
candle = Room('candle', 'There are unlit candles in the corner', [], {'e': 'starting'})
cold = Room('cold', 'It is cold, although there is a weird hole in the wall', [], {'w': 'starting', 'e': 'office'})
office = Room('office', 'There is a desk on the far side of the room', [], {'w': 'cold'})
skull = Room('skull', 'There is a skull in the corner', ['skull', 'bone'], {'s': 'starting'})
desk = Room('desk', 'Old desk', ['lighter', 'ciggarette'], {})

world = {'starting': starting,
         'candle': candle,
         'cold': cold,
         'office': office,
         'skull': skull,
         'desk': desk}
#Items
rskull = Item('skull', 'A pretty smooth skull')
lighter = Item('lighter', 'It is full of gas')
ciggarette = Item('ciggarette', 'Looks good enough to smoke')
bone = Item('bone', 'It is dirty')
key = Item('key', 'It is shiny')

items = {'skull': rskull,
         'lighter': lighter,
         'ciggarette': ciggarette,
         'bone': bone,
         'key': key}

def movement(direction, character): 
    newLocation = world[character.location.exits[direction]]
    character.location = newLocation

    print('--------------------')
    print('Location:', character.location)        
    print('Obvious Exits:', ', '.join(directions(character)))
    print('Visible Items:', visibleItems(character))
    print('Description:', character.location.description)

def directions(character):
    #Movement directions character can go  
    directions = []
    for k in character.location.exits.keys():
        if k == 'w':
            directions.append('west')
        if k == 'e':
            directions.append('east')
        if k == 'n':
            directions.append('north')
        if k == 's':
            directions.append('south')
    return directions

def visibleItems(character):
    if character.location == world['office']:
        if len(character.location.inv) == 0:
            return 'Desk'
        else:
            return ', '.join(character.location.inv) + ', Desk'
    elif len(character.location.inv) == 0:
        return 'None'
    else:
        return ', '.join(character.location.inv)
    
def prompt(character):
    command = input("\n> ").lower()
    validCommands = ['w', 'west', 'e', 'east', 'n', 'north', 's', 'south', 'help', 'quit', 'look', 'drop', 'pickup', 'use', 'inv', 'inventory']
    
    #adds commands for certain situations and extra commands
    if character.location == world['office']:
        validCommands.append('look desk')
    for x in character.inv:
        validCommands.append('look ' + x)
        validCommands.append('drop ' + x)
        validCommands.append('use ' + x)
    for x in character.location.inv:
        validCommands.append('pickup ' + x)

    if command in validCommands:
        #MOVEMENT
        if command in ['s', 'south'] and character.location == world['starting']:
            if starting.locked == False:
                character.escaped = True
            else:
                print("\nThe door is locked. You need to use a key!")
        elif command in ['w', 'west', 'e', 'east', 'n', 'north', 's', 'south'] and command not in directions(character):
            print('\nYou cannot go in this direction')
        elif command in directions(character) or command in character.location.exits.keys():
            if command == 'w' or command == 'west':
                movement('w', character)
            elif command == 'e' or command == 'east':
                movement('e', character)
            elif command == 'n' or command == 'north':
                movement('n', character)
            elif command == 's' or command == 'south':
                movement('s', character)
        #LOOK ROOM
        if len(command.split()) == 1 and command == 'look':
            print(character.location.look())
        #LOOK ITEMS
        if len(command.split()) == 2 and command.split()[0] == 'look':
            if command.split()[1] in items.keys():
                print(items[command.split()[1]].look())

            if command.split()[1] == 'desk' and character.location == world['office']:
                if len(desk.inv) == 0:
                    print("\nThe desk is empty so you close it.")
                else:
                    print("\nYou look inside of the desk, there is: " + ', '.join(desk.inv))
                    deskItems = []
                    for x in desk.inv:
                        deskItems.append(x)
                        
                    if len(desk.inv) == 2:
                        deskItems.append('both')
                    deskItems.append('none')
                    
                    print("What would you like take: " + ', '.join(deskItems))
                    item = input("> ").lower()

                    while item not in ['lighter', 'ciggarette', 'both', 'none']:
                        print("\nPlease select from: " + ', '.join(deskItems))
                        item = input("> ").lower()

                    if item == 'lighter':
                        print("You have picked up: Lighter")
                        character.inv.append('lighter')
                        desk.inv.remove('lighter')
                    elif item == 'ciggarette':
                        print("You have picked up: Ciggarette")
                        character.inv.append('ciggarette')
                        desk.inv.remove('ciggarette')
                    elif item == 'both':
                        print("You have picked up: Lighter and Ciggarette")
                        character.inv.append('lighter')
                        character.inv.append('ciggarette')
                        desk.inv.remove('lighter')
                        desk.inv.remove('ciggarette')
                    elif item == 'none':
                        print("You close the drawer leaving both items")
                
                    
        #PICKUP
        if len(command.split()) == 1 and command == 'pickup':
            if len(character.location.inv) == 0:
                print("\nThere is nothing to pickup.")
            else:
                print("\nWhat item would you like to pickup?")
                print("Type 'back' to cancel.")
                item = input("> ")
                while item not in character.location.inv and item != 'back':
                    print("\nThat item is not here. Try again")
                    item = input("> ")
                if item == 'back':
                    print("\nGone back")
                else:
                    character.pickup(item)
        if len(command.split()) == 2 and 'pickup' in command:
            if len(character.location.inv) == 0:
                print("\nThere is nothing to pickup.")
            else:
                if command.split()[1] in character.location.inv:
                    character.pickup(command.split()[1])
        #DROP
        if len(command.split()) == 1 and command == 'drop':
            if len(character.inv) == 0:
                print("\nThere is nothing to drop.")
            else:
                print("\nWhat item would you like to drop?")
                print("Type 'back' to cancel.")
                item = input("> ")
                while item not in character.inv and item != 'back':
                    print("\nThat item is not in your inventory. Try again")
                    item = input("> ")
                if item == 'back':
                    print("\nGone back")
                else:
                    character.drop(item)
        if len(command.split()) == 2 and 'drop' in command:
            if len(character.inv) == 0:
                print("\nThere is nothing to drop.")
            else:
                if command.split()[1] in character.inv:
                    character.drop(command.split()[1])   
        #USE
        if len(command.split()) == 1 and command == 'use':
            if len(character.inv) == 0:
                print("\nThere is nothing to use.")
            else:
                print("\nWhat item would you like to use?")
                print("Type 'back' to cancel.")
                item = input("> ")
                while item not in character.inv and item != 'back':
                    print("\nThat item is not in your inventory. Try again")
                    item = input("> ")
                if item == 'back':
                    print("\nGone back")
                else:
                    character.use(item)
        if len(command.split()) == 2 and 'use' in command:
            if len(character.inv) == 0:
                print("\nThere is nothing to drop.")
            else:
                if command.split()[1] in character.inv:
                    character.use(command.split()[1])
        #INVENTORY
        if command in ['inv', 'inventory']:
            print(character.getInventory())
        #HELP
        if command == 'help':
            print('look (item), use (item), drop (item), pickup (item), Direction(South, East, West, North), Inventory, Look, Quit')
            print('You can only look at items in your inventory')
        #QUIT
        if command == 'quit':
            quit()
    else:
        if len(command.split()) == 2 and command.split()[0] in ['look', 'use', 'drop', 'pickup']:
            if command.split()[1] not in character.inv and command.split()[1] not in character.location.inv:
                print("\nThat item is not valid. Try again")
        else:    
            print('\nThat is not a command if you dont know the commands, try "Help".')

def main():
    print("What would you like to name your character?")
    name = input("> ")
    
    character = Character(name, starting, [])

    print(F"Welcome {character.name}")
    
    print('--------------------')
    print('Location:', character.location)        
    print('Obvious Exits:', ', '.join(directions(character)))
    print('Visible Items:', visibleItems(character))
    print('Description:', character.location.description)

    while character.escaped == False:
        prompt(character)

    print("\nYou have escaped the room, Congratulations!")
    input("Press enter to end game.")
    quit()

main()

