# Elsa Lee Ting (S10205942H) - CSF01/P05
# Basic Program with Advancements
#-----------------------------------------------------------------------#
# This is a computer role-playing game called Ratventure.               #
# In this computer role-playing game, you will travel                   #
# around a grid map searching for the Orb of Power and                  #
# fighting rat minions. On the map are various towns where              #
# you can rest and save your game. Once you find the Orb of Power,      #
# destroy the Rat King to win the game. In this game, the towns         #
# and orb location are randomized every new game.                       #
#-----------------------------------------------------------------------#

from random import randint
import json

# +------------------------+ #
# | Text for various menus | #
# +------------------------+ #
main_text = ["New Game",\
             "Resume Game",\
             "View Leaderboard",\
             "Exit Game"]

town_text = ["View Character",\
             "View Map",\
             "Move",\
             "Rest",\
             "Save Game",\
             "Exit Game"]

open_text = ["View Character",\
             "View Map",\
             "Move",\
             "Sense Orb",\
             "Exit Game"]

fight_text = ["Attack",\
              "Run"] 

tryagain_text = ["Try again",\
                 "Exit game"] 

aftersaving_text = ["Continue",\
                    "Exit game"] 

map_data = [
    ['H/T', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', ' K '],
]

separator = '+---+---+---+---+---+---+---+---+\n'

# +-----------+ #
# | Variables | #
# +-----------+ #

# Player Statistics
player_stats = {'damage':[2,4], 'defence':1, 'health':20, 'orb': False, 'day': 1, 'location': 'town', 'player name': ''}

# Top Scores
top_scores = {}
current_player = []

# Enemy statistics
enemy_statistics = {'Rat' : {'damage': [1,3], 'defence': 1, 'health':10}, 'Cockroach' : {'damage': [2,4], 'defence': 2, 'health':15}, 'Rat King' : {'damage': [6,10], 'defence': 5, 'health': 25}}

# Current Enemy
current_enemy = ''

# List of locations where enemy has been defeated
defeated_locations = [[-1,-1]]

# Hero location
hero_c = 0
hero_r = 0

# Orb location
orb_c = 0
orb_r = 0

# Booleans
gameOver = False
stopFight = False


# +-----------+ #
# | Functions | #
# +-----------+ #

#~#~#~#~#~# Option Function #~#~#~#~#~#

# To loop through the menu texts and print out the options
def optionText(options):
    for option in range(len(options)):
        print('{}) {}'.format(option+1, options[option]))

#~#~#~#~#~#~#~#~#~#~#~#~#  Main Menu Functions #~#~#~#~#~#~#~#~#~#~#~#~#
# The Main Menu functions consists of functions for displaying         #
# the Main Menu, messages, 'New Game', 'Resume Game' and 'Exit Game'.  #
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~~#~#~#~#~#~#~#~#~#

# Function for printing the Main Menu
def displayMenu():
    print("Welcome to Ratventure!")
    print("----------------------")
    optionText(main_text)

### Function for the message ###
# This function will check if the hero is in town or outdoors and print the respective    #
# message. If the hero is outdoors, it will check if the hero has already fought the      #
# enemy in those coordinates. If he has, the outdoor menu will be printed, if not there   #
# will be an encounter will the same enemy. If the hero is in the same coordinates as the #
# Rat King, the rat king function will run.                                               #

def message():
    # Check if hero is in town or outdoors
    global hero_r, hero_c, stopFight
    if map_data[hero_r][hero_c] == 'H/T':
        print()
        message_text = 'Day {}: You are in a town.'.format(player_stats['day'])
        print(message_text)
        townMenu_choices()
        
    elif map_data[hero_r][hero_c] == ' H ':
        if stopFight == False:
            encounter()
        else:
            print()
            message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
            print(message_text)
            outdoorMenu_choices()

    elif map_data[hero_r][hero_c] == 'H/K':
        if stopFight == False:
            rat_king()
        else:
            print()
            message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
            print(message_text)
            outdoorMenu_choices()

# 1.1 Function for New Game
def newGame():
    global hero_r, hero_c, map_data, player_stats
    mapGrid()
    orbLocation()
    playerName()
    loadScore()
    message()

# Function to get player's name with input validation for top scores
def playerName():
    global player_stats
    while not gameOver:
        name = input('Enter your name: ')
        player_stats['player name'] = name
        if name.isalnum():
            player_stats['player name'] = name
            break
        else:
            print('Please enter your name without any spaces.')

# 1.2 Function for resume game
def resumeGame():
    message()
    orbLocation()

# 1.3 Function for exit game
def exitGame():
    print('Exiting...')
    exit()

# Function for top scores
def topScores():
    print()
    print(' Rank      Name     Score ')
    print('--------------------------')
    score_list = []
    counter = 1
    loadScore()
    for name_score in top_scores['top scores']:
        score_list.append([name_score[1], name_score[0]])
        score_list.sort()

    if len(score_list) >= 5:
        while counter <= 5:
            for i in range(5):
                print('|{:^6}|{:^10}|{:^6}|'.format(counter, score_list[i][1], score_list[i][0]))
                counter += 1
    else:
        for i in range(len(score_list)):
            print('|{:^6}|{:^12}|{:^6}|'.format(i+1, score_list[i][1], score_list[i][0]))

    print('--------------------------')
    print()

# Function to save score
def saveScore():
    global top_scores
    top_scores['top scores'] = current_player
    leaderboardfile = open('ratventure_leaderboard.json', 'w')
    leaderboardfile.write(json.dumps(top_scores))
    leaderboardfile.close()

# Function to load score with program validation
def loadScore():
    global top_scores, current_player
    try:
        leaderboardfile = open('ratventure_leaderboard.json', 'r')
        top_scores = json.loads(leaderboardfile.read())
        current_player = top_scores['top scores']
        leaderboardfile.close()

    except FileNotFoundError: 
        top_scores = {'top scores' : current_player}
        leaderboardfile = open('ratventure_leaderboard.json', 'w')
        leaderboardfile.write(json.dumps(top_scores))
        leaderboardfile.close()
 
# Functions for player to try again when he dies
def tryAgain():
    global player_stats, map_data, hero_r, hero_c
    player_stats = {'damage':[2,4], 'defence':1, 'health':20, 'orb': False, 'day': 1, 'location': 'town'}
    map_data = [
    ['H/T', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', ' K '],
]
    hero_c = 0
    hero_r = 0

    optionText(tryagain_text)
    tryagain_choice = input('Enter choice: ')
    if tryagain_choice == '1':
        print('New game!')
        newGame()
    elif tryagain_choice == '2':
        print('Exiting...')
        exit()


#~#~#~#~#~#~#~#~#~#~#~#~# Town Menu Functions  #~#~#~#~#~#~#~#~#~#~#~#~#
# The Town Menu functions consists of functions for displaying         #
# the Town Menu, 'View Character', 'View Map', 'Move', 'Rest',         #
# 'Save Game' and 'Exit Game'.                                         #
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~~#~#~#~#~#~#~#~#~#

# Function for the user to choose the Town Menu option
def townMenu_choices():
    while not gameOver:
        optionText(town_text)
        town_choice = input('Enter choice: ')

        # Input validation for the town choices
        if town_choice == '1':
            viewChar()
        elif town_choice == '2':
            printMap()
        elif town_choice == '3':
            move()
        elif town_choice == '4':
            rest()
        elif town_choice == '5':
            saveData()
        elif town_choice == '6':
            exitGame()
        else:
            print('Invalid choice. Please try again.')

    if gameOver == True:
        exit()

# Function for Viewing Character
def viewChar():
    charText = '''
The Hero
Damage: {}-{}
Defence: {}
HP: {}'''.format(player_stats['damage'][0], player_stats['damage'][1], player_stats['defence'], player_stats['health'])
    print(charText)

    if player_stats['orb'] == True:
        print('You are holding the Orb of Power.')

    if stopFight == True:
        encounter()
    else:
        message()

### Functions for Viewing Map ###
# Function to randomize the towns and to place them in the map data. The towns are randomized by first #
# getting random coordinates for the town. Then, the function will check if all the towns are at least #
# 3 steps away from each other. If they are not, the function will loop again and generate another set #
# of coordinates until there are four towns.                                                           #

def mapGrid():
    global map_data
    town = 0
    #Check if the town can be placed
    while True:
        canPlace = True
        x = randint(0,7)
        y = randint(0,7)
        for column in range(-2,3):
            start = abs(column) - 2
            end = abs(start) + 1

            for row in range(start, end):
                if not (0 <= x + column <= 7 and 0 <= y + row <= 7): 
                    continue

                if map_data[x+column][y+row] != '   ':
                    canPlace = False
                    break

        if canPlace == True:
            map_data[x][y] = ' T '
            town += 1
        if town == 4:
            break
        
# Function for printing the map
def printMap():
    gridText = ''
    gridText += separator 
    for row in range(8):
        gridText += '|'+'|'.join(map_data[row])+'|\n'
        gridText += separator 

    print(gridText)

    if stopFight == True:
        encounter()
    else:
        message()

### Functions for Move ###
# This function will first print the map of the hero's current location.         #
# Then it will get the user's choice. If the input in invalid, it will ask for   #
# another input. Then, according to where the hero moves, the map_data list will #
# change to show the new map with the hero's new location.                       #

def move():
    global hero_r, hero_c, map_data
    # Print map
    gridText = ''
    gridText += separator 
    for row in range(8):
        gridText += '|'+'|'.join(map_data[row])+'|\n'
        gridText += separator

    print(gridText)
    print('W = up; A = left; S = down; D = right')
    move_choice = input('Your move: ')

    # Input validation for the moving choices
    while True:
        if map_data[hero_r][hero_c] == 'H/T':
            map_data[hero_r][hero_c] = ' T '
        elif map_data[hero_r][hero_c] == ' H ':
            map_data[hero_r][hero_c] = '   '
        elif map_data[hero_r][hero_c] == 'H/K':
            map_data[hero_r][hero_c] = ' K '

        if move_choice == 'w':
            if hero_r == 0:
                print('Player cannot move up. Please try again.')
                move_choice = input('Your move: ')
            else:
                hero_r -= 1
                break

        elif move_choice == 's':
            if hero_r == 7:
                print('Player cannot move down. Please try again.')
                move_choice = input('Your move: ')
            else:
                hero_r += 1
                break

        elif move_choice == 'a':
            if hero_c == 0:
                print('Player cannot move left. Please try again.')
                move_choice = input('Your move: ')
            else:
                hero_c -= 1
                break

        elif move_choice == 'd':
            if hero_c == 7:
                print('Player cannot move right. Please try again.')
                move_choice = input('Your move: ')
            else:
                hero_c += 1
                break
        else:
            print('Invalid choice. Please try again.')
            move_choice = input('Your move: ')

    if map_data[hero_r][hero_c] == '   ':
        map_data[hero_r][hero_c] = ' H ' 
    elif map_data[hero_r][hero_c] == ' T ':
        map_data[hero_r][hero_c] = 'H/T' 
    elif map_data[hero_r][hero_c] == ' K ':
        map_data[hero_r][hero_c] = 'H/K' 

    # Print map
    gridText = ''
    gridText += separator 
    for row in range(8):
        gridText += '|'+'|'.join(map_data[row])+'|\n'
        gridText += separator
    print(gridText)
    nextDay_move()
    message()
 
# Function for the next day after user moves to add a day and reset current enemy.
def nextDay_move():
    global current_enemy
    player_stats['day'] += 1
    current_enemy = ''

# 2.4 Functions for Rest
def rest():
    global player_stats
    player_stats['health'] = 20
    print()
    print('You are fully healed!')
    player_stats['day'] += 1 
    message()

# 2.5 Functions for Save and Load using json
def saveData():
    global gameOver
    playerData = {'map': map_data, 'player_stats': player_stats, 'hero_r': hero_r, 'hero_c': hero_c}
    savefile = open('ratventure_save.json', 'w')
    savefile.write(json.dumps(playerData))
    savefile.close()
    print('Game saved.')
    afterSaving()

def loadData():
    global player_stats, map_data, hero_r, hero_c
    try:
        savefile = open('ratventure_save.json', 'r')
        raw_data = savefile.read()
        playerData = json.loads(raw_data)
        map_data = playerData['map']
        player_stats = playerData['player_stats']
        hero_c = playerData['hero_c']
        hero_r = playerData['hero_r']
        savefile.close()

    except:
        print('No save file. Start a new game.')
        print()

    else:
        resumeGame()

def afterSaving():
    print()
    print('Would you like to continue playing or exit?')
    optionText(aftersaving_text)
    aftersaving_choice = input('Enter choice: ')
    if aftersaving_choice == '1':
        message()
    elif aftersaving_choice == '2':
        print('Exiting...')
        exit()

# 2.6 Function for Exit Game
    # Use the same function as the one for Main Menu


#~#~#~#~#~#~#~#~#~#~#  Combat Menu Functions #~#~#~#~#~#~#~#~#~#~#~#
# The Combat Menu functions consists of functions for displaying   #
# the Combat Menu, randomizing enemies, 'Attack' and 'Run'.        #
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~~#~#~#~#~#~#~#

### Function to randomize encounters ###
# This function will check if there is an enemy in the location that the hero is in        #
# in case the hero has already defeated the enemy inside. The function will then generate  #
# a random chance for an enemy to appear. The game will also have two different types of   #
# enemies that will be randomly generated with a 50/50 chance. If there is no enemy in the #
# location, the function will run the normal outdoor menu.                                 #

def encounter():
    global current_enemy, defeated_locations, hero_c, hero_r
    defeatedLocation = False
    have_enemy = False
    chance = randint(0,100)

    # Check if there is an enemy in the location
    for i in range(len(defeated_locations)):

        if defeated_locations[i][0] == hero_r and defeated_locations[i][1] == hero_c:
            defeatedLocation = True
            nextMove()

    
    if defeatedLocation == False:
        if current_enemy == '':
            if 70 > chance:
            # Generate random enemy 
                have_enemy = True
                enemyList = list(enemy_statistics.keys())
                random_enemy = randint(0, len(enemyList)-2)
                current_enemy = enemyList[random_enemy]
            
        else:
            have_enemy = True

        if have_enemy == True:
            enemyStats = enemy_statistics[current_enemy]
            message_text = '''
Day {}: You are out in the open.
Encounter! - {}
Damage: {}-{}
Defence:  {}
HP: {}'''.format(player_stats['day'], current_enemy, enemyStats['damage'][0], enemyStats['damage'][1], enemyStats['defence'], enemyStats['health'])  
            
            print(message_text)
            combatMenu()

        else:
            #No rat when chance not met
            message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
            print(message_text)
            outdoorMenu_choices()

## Combat Menu (Attack or Run)

# Function for printing the combat choices
def combatMenu():
    optionText(fight_text)
    combatMenu_choices()


# Function for the user to choose the Combat Menu option
def combatMenu_choices():
    while not gameOver:

        fight_choice = input('Enter choice: ')
        if fight_choice == '1':
            attack()

        elif fight_choice == '2':
            run()
            break

        else:
            print('Invalid choice. Please try again.')

    if gameOver == True:
        exit()


### 3.1 Function for Attack ###
# This function will be called when the player chooses to attack. The enemy damage will      #
# be a random amount between his min damage and his max damage, reduced by the hero's        #
# defence. The hero damage will also be a random amount between his min damage and his max   #
# damage, reduced by the enemy's defence. If the enemy health is reduced to 0 or less, the   #
# enemy will die and the hero will be able to move on to the next move. If the hero's health #
# is reduced to 0 or less, the hero will die and the game will end.                          #

def attack():
    global current_enemy, enemy_statistics, gameOver, stopFight, top_scores, current_player

    #Enemy damage
    enemyStats = enemy_statistics[current_enemy]
    random_enemy_damage = randint(enemyStats['damage'][0], enemyStats['damage'][1])
    
    if random_enemy_damage >= player_stats['defence']:
        enemy_damage = random_enemy_damage - player_stats['defence']

    else:
        enemy_damage = 0

    if player_stats['orb'] == False and current_enemy == 'Rat King':
        # Hero damage
        random_hero_damage = 0
        print()
        combat_text = 'You do not have the Orb of Power - the Rat King is immune!'
        print(combat_text)

    else:
    # Hero damage
        random_hero_damage = randint(player_stats['damage'][0], player_stats['damage'][1])

    if random_hero_damage >= enemyStats['defence']:
        hero_damage = random_hero_damage - enemyStats['defence']
    
    else:
        hero_damage = 0


    enemyStats['health'] = enemyStats['health'] - hero_damage

    if current_enemy == 'Rat King' and enemyStats['health'] <= 0:
        combat_text = '''
The Rat King is dead! You are victorious!
Congratulations, you have defeated the Rat King!
The world is saved! You win!'''
        print(combat_text)
        current_player.append([player_stats['player name'], player_stats['day']])
        saveScore()
        gameOver = True

    elif enemyStats['health'] <= 0 and current_enemy != 'Rat King':
        stopFight = True
        combat_text = 'The {} is dead! You are victorious!'.format(current_enemy)
        enemy_statistics = {'Rat' : {'damage': [1,3], 'defence': 1, 'health':10}, 'Cockroach' : {'damage': [2,4], 'defence': 2, 'health':15}, 'Rat King' : {'damage': [6,10], 'defence': 5, 'health': 25}}
        defeated_locations.append([hero_r,hero_c])
        current_enemy = ''
        print(combat_text)
        message()

    else:
        player_stats['health'] = player_stats['health'] - enemy_damage

        if player_stats['health'] <= 0:
            combat_text = '''\
You have been defeated by the {}!
Game Over. Try again?'''.format(current_enemy)
            print(combat_text)
            tryAgain()
            gameOver = True

        else:
            combat_text = '''
You deal {} damage to the {}!
Ouch! the {} hit you for {} damage!
            '''.format(hero_damage, current_enemy, current_enemy, enemy_damage)
            message_text = '''\
Day {}: You are out in the open.
Encounter! - {}
Damage: {}-{}
Defence:  {}
HP: {}
-----------------------
You have {} HP left.
'''.format(player_stats['day'],current_enemy, enemyStats['damage'][0], enemyStats['damage'][1], enemyStats['defence'], enemyStats['health'], player_stats['health'])
            print(combat_text)
            print(message_text)
            combatMenu()

# Next move if enemy is defeated
def nextMove():
    message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
    print(message_text)

# 3.2 Function for Run 
# This function will reset the enemy's health so that when the player encounters #
# it again. The enemy will be at full health.                                    #
def run():
    global enemy_statistics, stopFight
    enemy_statistics = {'Rat' : {'damage': [1,3], 'defence': 1, 'health':10}, 'Cockroach' : {'damage': [2,4], 'defence': 2, 'health':15}, 'Rat King' : {'damage': [6,10], 'defence': 5, 'health': 25}}
    print('You run and hide.')
    stopFight = True
    message()

    
#~#~#~#~#~#~#~#~#~# Outdoor Menu Functions #~#~#~#~#~#~#~#~#~#
# The Outdoor Menu functions consists of functions for       #
# displaying the Outdoor Menu, randomizing the orb location  #
# and 'Sense Orb'.                                           #
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~~#~#~#~#


# 4.1-4.3 uses the same functions as the ones in the Town Menu

# Function for the user to choose the Outdoor Menu option
def outdoorMenu_choices():
    global stopFight
    stopFight = False
    while not gameOver:
        optionText(open_text)
        outdoor_choice = input('Enter choice: ')

        # Input validation for the outdoor choices
        if outdoor_choice == '1':
            viewChar()
        elif outdoor_choice == '2':
            printMap()
        elif outdoor_choice == '3':
            move()
        elif outdoor_choice == '4':
            senseOrb()
        elif outdoor_choice == '5':
            exitGame()
        else:
            print('Invalid choice. Please try again.')

    if gameOver == True:
        exit()

### Function to generate random orb location ###
# This function will generate random orb coordinates using randint. Then it will check #
# if the orb location is valid. If the orb is in any of the squares at the 4 rightmost #
# columns or bottommost rows or/and the orb is not in an empty space, the orb will not #
# be placed and a new location will be generated.                                      #
 
def orbLocation():
    global orb_r, orb_c
    cannotPlace = True
    while cannotPlace == True:
        orb_c = randint(0,7)
        orb_r = randint(0,7)
        if (orb_c <= 3 and orb_r <= 3) or map_data[orb_r][orb_c] != '   ':
            cannotPlace = True
        else:
            break

### 4.4 Function for player to sense orb ###
# This function will check if the hero coordinates are the same as the orb coordinates.  #
# If the hero is in the same location as the orb, the hero's damage and defence will     #
# increase by 5. If the player has not found the orb, the direction of the orb will be   #
# provided. If the player already has the orb and senses for it, the function will print #
# a message to tell the player that he has the orb.                                      #

def senseOrb():
    print()
    global player_stats
    if player_stats['orb'] == False:
        if hero_r == orb_r and hero_c == orb_c:
            player_stats['damage'][0] += 5
            player_stats['damage'][1] += 5
            player_stats['defence'] +=5
            player_stats['orb'] = True
            senseOrb_text = '''
You found the Orb of Power!
Your attack increases by 5!
Your defence increases by 5!

The Hero
Damage: {}-{}
Defence: {}
HP: {}

You are holding the Orb of Power.'''.format(player_stats['damage'][0], player_stats['damage'][1], player_stats['defence'], player_stats['health'])

        else:
            direction = ''
            if orb_r < hero_r:
                direction += 'North'
            elif orb_r > hero_r:
                direction += 'South'
            if orb_c > hero_c:
                direction += 'East'
            elif orb_c < hero_c:
                direction += 'West'
            senseOrb_text = '''

You sense that the Orb of Power
is to the {}.
'''.format(direction)

    else:
        senseOrb_text = 'You are holding the Orb of Power.'

    print(senseOrb_text)
    nextDay_sense()

# Function for the next day after sensing orb
def nextDay_sense():
    player_stats['day'] += 1
    message()

# 4.5 Function for Exit Game
    # Use the same function as the one for Main Menu


#~#~#~#~#~# The Rat King Function #~#~#~#~#~#
# Rat King uses the same functions as the ones in Combat Menu
# 5.1 + 5.2: 
def rat_king():
    global player_stats, enemy_statistics, current_enemy
    current_enemy = 'Rat King'
    encounter()


############## Loop for the game to continue ##############
while not gameOver:
    displayMenu()
    choice = input('Enter choice: ')

    if choice == '1':
        newGame()
    elif choice == '2':
        loadData()
    elif choice == '3':
        topScores()
    elif choice == '4':
        exitGame()
    else:
        print('Invalid choice. Please try again.')

if gameOver == True:
    exit()
#---------------------------------------------------------#