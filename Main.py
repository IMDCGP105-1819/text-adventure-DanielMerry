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
        pass

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

    def look(self):
        return self.description

    def __str__(self):
        return self.name + ' room'

    def __repr__(self):
        return str(self)

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
starting = Room('starting', 'Dark and moist', ['key'], {'w': 'candle', 'n': 'skull', 'e': 'cold'})
candle = Room('candle', 'There are unlit candles in the corner', [], {'e': 'starting'})
cold = Room('cold', 'It is cold, although there is a weird hole in the wall', [], {'w': 'starting', 'e': 'office'})
office = Room('office', 'There is a desk on the far side of the room', [], {'w': 'cold'})
skull = Room('skull', 'There is a skull in the corner', [], {'s': 'starting'})

world = {'starting': starting,
         'candle': candle,
         'cold': cold,
         'office': office,
         'skull': skull}
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
    if len(character.location.inv) == 0:
        return 'None'
    else:
        return ', '.join(character.location.inv)
    
def prompt(character):
    command = input("\n> ").lower()
    validCommands = ['w', 'west', 'e', 'east', 'n', 'north', 's', 'south', 'help', 'quit', 'look', 'drop', 'pickup']

    #adds the commends for look, drop and pickup
    for x in character.inv:
        validCommands.append('look ' + x)
        validCommands.append('drop ' + x)
    for x in character.location.inv:
        validCommands.append('pickup ' + x)
    
    if command in validCommands:
        #MOVEMENT
        if command in ['w', 'west', 'e', 'east', 'n', 'north', 's', 'south'] and command not in directions(character):
            print('\nYou cannot go in this direction')
        if command in directions(character) or command in character.location.exits.keys():
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
        #PICKUP
        if len(command.split()) == 1 and command == 'pickup':
            if len(character.location.inv) == 0:
                print("\nThere is nothing to pickup.")
            else:
                print("\nWhat item would you like to pickup?")
                print("Type 'back' to cancel.")
                item = input("> ")
                while item not in character.location.inv and item != 'back':
                    print("\nThat item is not here.")
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
                    print("\nThat item is not here.")
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
        
        #HELP
        if command == 'help':
            print('Try:', ', '.join(validCommands))
            print('You can only look at items in your inventory')
        #QUIT
        if command == 'quit':
            quit()
    else:
        print('\nThat is not a command if you dont know the commands, try "Help".')

def main():      
    character = Character('Daniel', starting, ['key'])

    print(F"Welcome {character.name}")
    
    print('--------------------')
    print('Location:', character.location)        
    print('Obvious Exits:', ', '.join(directions(character)))
    print('Visible Items:', visibleItems(character))

    while character.escaped == False:
        prompt(character)

main()

