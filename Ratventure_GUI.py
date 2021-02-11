# Elsa Lee Ting (S10205942H) - CSF01/P05
# GUI 
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
from tkinter import *
from tkinter import messagebox 
import json

#########################################
#-------------- VARIABLES --------------#
#########################################

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

# Map Data
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

# Hero location
hero_c = 0
hero_r = 0

# Orb location
orb_c = 0
orb_r = 0

#########################################
#-------------- FUNCTIONS --------------#
#########################################

### Main Menu functions ###
# 1.1 New Game
def newGame():
    enterName_frame.place(x=0,y=0)
    entryName.delete('0', END)
    mapGrid()
    orbLocation()
    message()
    loadScore()

# 1.2 Resume Game
def resumeGame():
    newGame_frame.place(x=0,y=0)
    message()
    orbLocation()

# 1.3 Exit Game
def exitGame():
    exit()

# Function for top scores
def topScores():
    topScores_frame.place(x=0,y=0)
    returnButton.place(x=230,y=600)
    score_list = []
    counter = 1
    loadScore()
    score_message = ''
    score_message += 'Rank      Name     Score\n' 
    score_message += '--------------------------\n'
    for name_score in top_scores['top scores']:
        score_list.append([name_score[1], name_score[0]])
        score_list.sort()

    if len(score_list) >= 5:
        while counter <= 5:
            for i in range(5):
                score_message += '|{:^6}|{:^10}|{:^6}|\n'.format(counter, score_list[i][1], score_list[i][0])
                counter += 1
    else:
        for i in range(len(score_list)):
            score_message += '|{:^6}|{:^10}|{:^6}|\n'.format(i+1, score_list[i][1], score_list[i][0])
    
    score_message += '--------------------------'
    scoreText.configure(state = 'normal')
    scoreText.delete('1.0',END)
    scoreText.insert('end', score_message)
    scoreText.configure(state = 'disabled')

def returnBack():
    topScores_frame.place_forget()

def saveScore():
    global top_scores
    top_scores['top scores'] = current_player
    leaderboardfile = open('ratventure_leaderboard.json', 'w')
    leaderboardfile.write(json.dumps(top_scores))
    leaderboardfile.close()

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
 
# Function for player to enter name
def playerName():
    global player_stats
    if entryName.get().isalnum():
        player_stats['player name'] = entryName.get()
        enterName_frame.place_forget
        newGame_frame.place(x=0,y=0)
    else:
        messagebox.showinfo(title='Error', message='Please enter your name without any spaces.')

# Function for the message
def message():
    dayText.delete('1.0', 'end')

    # Check if hero is in town or outdoors
    global hero_r,hero_c
    if map_data[hero_r][hero_c] == 'H/T':
        message_text = 'Day {}: You are in a town.'.format(player_stats['day'])
        senseButton.place_forget()
        restButton.place(x=250,y=420)
        saveButton.place(x=250,y=510)
        exitButton.place(x=250,y=600)
        
        dayText.configure(state = 'normal')
        dayText.delete('1.0',END)
        dayText.insert('end', message_text)
        dayText.configure(state = 'disabled')   

    elif map_data[hero_r][hero_c] == ' H ':
        encounter()

    elif map_data[hero_r][hero_c] == 'H/K':
        rat_king()

#~#~#~#~#~# Town Menu Functions #~#~#~#~#~#

# 2.1 View Character
def playerStats():
    viewChar_frame.place(x=0,y=0)
    statsText.delete('1.0', 'end')
    text = '''
    The Hero
    Damage: {}-{}
    Defence: {}
    HP: {}'''.format(player_stats['damage'][0], player_stats['damage'][1], player_stats['defence'], player_stats['health'])
    backButton = Button(viewChar_frame, text = 'Back', width = 10, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'light gray', command = goBack_player)
    backButton.place(x=10,y=20)
    statsText.configure(state = 'normal')
    statsText.delete('1.0',END)
    statsText.insert('end', text)
    statsText.configure(state = 'disabled')

# Back button function after viewing player stats
def goBack_player():
    global current_enemy
    viewChar_frame.place_forget()
    if current_enemy != '':
        encounter()

# 2.2 View Map
def mapGrid():
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
        
# Print map
def printMap():
    viewMap_frame.place(x=0,y=0)
    # Top Line
    gridText = ''
    gridText += separator 
    for row in range(8):
        gridText += '|'+'|'.join(map_data[row])+'|\n'
        gridText += separator

    mapText.configure(state = 'normal')
    mapText.delete('1.0',END)
    mapText.insert('end', gridText)
    mapText.configure(state = 'disabled')

# Back button function after viewing player stats
def goBack_map():
    viewMap_frame.place_forget()
    if current_enemy != '':
        encounter()

# 2.3 Move
def move():
    move_frame.place(x=0,y=0)
    
    upButton =  Button(move_frame, text = '🡹', width = 5, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = up_Button)
    upButton.place(x=200,y=200)
    downButton =  Button(move_frame, text = '🡻', width = 5, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = down_Button)
    downButton.place(x=200,y=500)
    leftButton =  Button(move_frame, text = '🡸', width = 5, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = left_Button)
    leftButton.place(x=100,y=350)
    rightButton =  Button(move_frame, text = '🡺', width = 5, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = right_Button)
    rightButton.place(x=300,y=350)
    mapText_move = Text(move_frame, width=40, height=20, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0) 
    mapText_move.place(x=600,y=100)

    # Check if player can move
    if hero_r == 0:
        upButton['state']='disabled'
    if hero_r == 7:
        downButton['state']='disabled'
    if hero_c == 0:
        leftButton['state']='disabled'
    if hero_c == 7:
        rightButton['state']='disabled'

    # Print map
    gridText = ''
    gridText += separator 
    for row in range(8):
        gridText += '|'+'|'.join(map_data[row])+'|\n'
        gridText += separator

    mapText_move.configure(state = 'normal')
    mapText_move.delete('1.0',END)
    mapText_move.insert('end', gridText)
    mapText_move.configure(state = 'disabled')

### Button functions ###
# Up
def up_Button():
    global hero_r, hero_c
    if map_data[hero_r][hero_c] == 'H/T':
        map_data[hero_r][hero_c] = ' T '
    elif map_data[hero_r][hero_c] == ' H ':
        map_data[hero_r][hero_c] = '   '
    elif map_data[hero_r][hero_c] == 'H/K':
        map_data[hero_r][hero_c] = ' K '

    hero_r -= 1
    if map_data[hero_r][hero_c] == '   ':
       map_data[hero_r][hero_c] = ' H ' 
    elif map_data[hero_r][hero_c] == ' T ':
        map_data[hero_r][hero_c] = 'H/T' 
    elif map_data[hero_r][hero_c] == ' K ':
        map_data[hero_r][hero_c] = 'H/K' 

    nextDay_move()

# Down
def down_Button():
    global hero_r, hero_c
    if map_data[hero_r][hero_c] == 'H/T':
        map_data[hero_r][hero_c] = ' T '
    elif map_data[hero_r][hero_c] == ' H ':
        map_data[hero_r][hero_c] = '   '
    elif map_data[hero_r][hero_c] == 'H/K':
        map_data[hero_r][hero_c] = ' K '

    hero_r += 1
    if map_data[hero_r][hero_c] == '   ':
        map_data[hero_r][hero_c] = ' H ' 
    elif map_data[hero_r][hero_c] == ' T ':
        map_data[hero_r][hero_c] = 'H/T' 
    elif map_data[hero_r][hero_c] == ' K ':
        map_data[hero_r][hero_c] = 'H/K'

    nextDay_move()

# Left
def left_Button():
    global hero_r, hero_c
    if map_data[hero_r][hero_c] == 'H/T':
        map_data[hero_r][hero_c] = ' T '
    elif map_data[hero_r][hero_c] == ' H ':
        map_data[hero_r][hero_c] = '   '
    elif map_data[hero_r][hero_c] == 'H/K':
        map_data[hero_r][hero_c] = ' K '

    hero_c -= 1
    if map_data[hero_r][hero_c] == '   ':
        map_data[hero_r][hero_c] = ' H ' 
    elif map_data[hero_r][hero_c] == ' T ':
        map_data[hero_r][hero_c] = 'H/T' 
    elif map_data[hero_r][hero_c] == ' K ':
        map_data[hero_r][hero_c] = 'H/K' 

    nextDay_move()

# Right
def right_Button():
    global hero_r, hero_c
    if map_data[hero_r][hero_c] == 'H/T':
        map_data[hero_r][hero_c] = ' T '
    elif map_data[hero_r][hero_c] == ' H ':
        map_data[hero_r][hero_c] = '   '
    elif map_data[hero_r][hero_c] == 'H/K':
        map_data[hero_r][hero_c] = ' K '

    hero_c += 1
    if map_data[hero_r][hero_c] == '   ':
        map_data[hero_r][hero_c] = ' H ' 
    elif map_data[hero_r][hero_c] == ' T ':
        map_data[hero_r][hero_c] = 'H/T' 
    elif map_data[hero_r][hero_c] == ' K ':
        map_data[hero_r][hero_c] = 'H/K'
    
    nextDay_move()

# Next day after move
def nextDay_move():
    global current_enemy
    move_frame.place_forget()
    player_stats['day'] += 1
    current_enemy = ''
    message()

# 2.4 Rest
def rest():
    global player_stats
    rest_frame.place(x=0,y=0)
    player_stats['health'] = 20
    healthLabel = Label(rest_frame, text = 'You are fully healed!', width=40, height=10, font = ('fixedsys', '40'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0) 
    healthLabel.place(x=20,y=50)
    nextdayButton_rest =  Button(rest_frame, text = 'Next Day', width = 10, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'light gray', command = nextDay_rest)
    nextdayButton_rest.place(x=1000,y=500)

# Next day after rest 
def nextDay_rest():
    rest_frame.place_forget()
    player_stats['day'] += 1    
    message()

# 2.5 Save (and Load)
def saveData():
    playerData = {'map': map_data, 'player_stats': player_stats, 'hero_r': hero_r, 'hero_c': hero_c}
    savefile = open('ratventure_save.json', 'w')
    savefile.write(json.dumps(playerData))
    savefile.close()
    messagebox.showinfo(title='Save', message='Game Saved')

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
        resumeGame()
    except:
        messagebox.showinfo(title='Error', message='No save file. Start a new game.')

#~#~#~#~#~# Outdoor Menu functions #~#~#~#~#~#

# Generate orb location
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

# Sense orb
def senseOrb():
    global player_stats
    sense_frame.place(x=0,y=0)
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
    is to the {}.'''.format(direction)

    else:
        senseOrb_text = 'You are holding the Orb of Power.'

    senseText.delete('1.0', 'end')
    senseText.configure(state = 'normal')
    senseText.delete('1.0',END)
    senseText.insert('end', senseOrb_text)
    senseText.configure(state = 'disabled')

    # Next day before
    nextdayButton_sense =  Button(sense_frame, text = 'Next Day', width = 10, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'light gray', command = nextDay_sense)
    nextdayButton_sense.place(x=1000,y=500)

# Next day after sense orb
def nextDay_sense():
    sense_frame.place_forget()
    player_stats['day'] += 1
    message()

#~#~#~#~#~# Combat Menu Functions #~#~#~#~#~#

# Encounter 
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

            characterButton.place_forget()
            mapButton.place_forget()
            moveButton.place_forget()
            restButton.place_forget()
            senseButton.place_forget()
            saveButton.place_forget()
            exitButton.place_forget()
            attackButton.place(x=800,y=300)
            runButton.place(x=800,y=450)
                                                            
        else:
            #No rat when chance not met
            message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
            restButton.place_forget()
            senseButton.place(x=250,y=420)

        dayText.configure(state = 'normal')
        dayText.delete('1.0',END)
        dayText.insert('end', message_text)
        dayText.configure(state = 'disabled')

# Attack 
def attack():
    combat_frame.place(x=0,y=0)
    global current_enemy, enemy_statistics, top_scores, current_player, player_stats
    mainmenuButton.place_forget()
    combat_text = ''

    #Enemy damage
    enemyStats = enemy_statistics[current_enemy]
    random_enemy_damage = randint(enemyStats['damage'][0], enemyStats['damage'][1])

    if random_enemy_damage >= player_stats['defence']:
        enemy_damage = random_enemy_damage - player_stats['defence']
    
    else:
        enemy_damage = 0


    if player_stats['orb'] == False and current_enemy == 'Rat King':
        # Hero damage
        hero_damage = 0
        combat_text += '''
You do not have the Orb of Power!
The Rat King is immune!'''

    else:
    # Hero damage
        random_hero_damage = randint(player_stats['damage'][0], player_stats['damage'][1])

        if random_hero_damage >= enemyStats['defence']:
            hero_damage = random_hero_damage - enemyStats['defence']
    

    enemyStats['health'] = enemyStats['health'] - hero_damage


    nextButton.place_forget()
    continueButton.place(x=150,y=500)

    if current_enemy == 'Rat King' and enemyStats['health'] <= 0:
        combat_text += '''
The Rat King is dead! 
You are victorious!
Congratulations!
The world is saved! You win!'''
        current_player.append([player_stats['player name'], player_stats['day']])
        saveScore()
        mainmenuButton.place(x=150,y=500)
        continueButton.place_forget()


    elif enemyStats['health'] <= 0 and current_enemy != 'Rat King':
        combat_text += 'Victory!'
        continueButton.place_forget()
        nextButton.place(x=150,y=400)
        enemy_statistics = {'Rat' : {'damage': [1,3], 'defence': 1, 'health':10}, 'Cockroach' : {'damage': [2,4], 'defence': 2, 'health':15}, 'Rat King' : {'damage': [6,10], 'defence': 5, 'health': 25}}
        defeated_locations.append([hero_r,hero_c])
        current_enemy = ''
    
    else:
        player_stats['health'] = player_stats['health'] - enemy_damage

        if player_stats['health'] <= 0:
            combat_text += '''
You have been defeated
by the {}!
Game Over.'''.format(current_enemy)
            continueButton.place_forget()
            mainmenuButton.place(x=150,y=500)
        
        else:
            combat_text += '''
You deal {} damage to the {}!
Ouch! the {} hit you
for {} damage!'''.format(hero_damage, current_enemy, current_enemy, enemy_damage)
            message_text = '''\
Day {}: You are out in the open.
Encounter! - {}
Damage: {}-{}
Defence:  {}
HP: {}
-----------------------
You have {} HP left.'''.format(player_stats['day'],current_enemy, enemyStats['damage'][0], enemyStats['damage'][1], enemyStats['defence'], enemyStats['health'], player_stats['health'])

            dayText.configure(state = 'normal')
            dayText.delete('1.0',END)
            dayText.insert('end', message_text)
            dayText.configure(state = 'disabled')


    combatText.configure(state = 'normal')
    combatText.delete('1.0',END)
    combatText.insert('end', combat_text)
    combatText.configure(state = 'disabled')



# Continue the fight if enemy is still alive
def continueFight():
    combat_frame.place_forget()

# Next move if enemy is defeated
def nextMove():
    combat_frame.place_forget()
    characterButton.place(x=250,y=150)
    mapButton.place(x=250,y=240)
    moveButton.place(x=250,y=330)
    senseButton.place(x=250,y=420)
    exitButton.place(x=250,y=510)
    attackButton.place_forget()
    runButton.place_forget()
    mainmenuButton.place_forget()
    
    message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
    dayText.configure(state = 'normal')
    dayText.delete('1.0',END)
    dayText.insert('end', message_text)
    dayText.configure(state = 'disabled')

# Game end if Hero dies
def returnMainMenu():
    global player_stats, map_data, hero_r, hero_c
    player_stats = {'damage':[2,4], 'defence':1, 'health':20, 'orb': False, 'day': 1, 'location': 'town'}
    combat_frame.place_forget()
    newGame_frame.place_forget()
    enterName_frame.place_forget()
    characterButton.place(x=250,y=150)
    mapButton.place(x=250,y=240)
    moveButton.place(x=250,y=330)
    restButton.place(x=250,y=420)
    saveButton.place(x=250,y=510)
    exitButton.place(x=250,y=600)
    attackButton.place_forget()
    runButton.place_forget()
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
    message_text = 'Day {}: You are in a town.'.format(player_stats['day'])
    dayText.configure(state = 'normal')
    dayText.delete('1.0',END)
    dayText.insert('end', message_text)
    dayText.configure(state = 'disabled')

# Run
def run():
    global enemy_statistics
    characterButton.place(x=250,y=150)
    mapButton.place(x=250,y=240)
    moveButton.place(x=250,y=330)
    senseButton.place(x=250,y=420)
    exitButton.place(x=250,y=510)
    attackButton.place_forget()
    runButton.place_forget()
    mainmenuButton.place_forget()
    enemy_statistics = {'Rat' : {'damage': [1,3], 'defence': 1, 'health':10}, 'Cockroach' : {'damage': [2,4], 'defence': 2, 'health':15}, 'Rat King' : {'damage': [6,10], 'defence': 5, 'health': 25}}

    message_text = 'Day {}: You are out in the open.'.format(player_stats['day'])
    dayText.configure(state = 'normal')
    dayText.delete('1.0',END)
    dayText.insert('end', message_text)
    dayText.configure(state = 'disabled')

#~#~#~#~#~# Rat King Function #~#~#~#~#~#
def rat_king():
    global player_stats, enemy_statistics, current_enemy
    current_enemy = 'Rat King'
    encounter()


###################################
#-------------- GUI --------------#
###################################

# Main menu
window = Tk()
window.title('Ratventure')
window.geometry('1366x768')
#window.attributes("-fullscreen", True)
window.configure(bg = 'lightskyblue')

titleLabel = Label(window, text = 'Welcome to Ratventure', width = 25, font = ('fixedsys', '80', 'bold'), fg = 'royal blue', bg = 'lightskyblue')
titleLabel.place(x=150,y=80)

newgameButton = Button(window, text = 'New Game', width = 30, font = ('fixedsys', '30', 'bold'), fg = 'royal blue', bg = 'light gray', command = newGame)
newgameButton.place(x=280,y=300)

resumegameButton = Button(window, text = 'Resume Game', width = 30, font = ('fixedsys', '30', 'bold'), fg = 'royal blue', bg = 'light gray', command = loadData)
resumegameButton.place(x=280,y=400)

topscoresButton = Button(window, text = 'Top Scores', width = 30, font = ('fixedsys', '30', 'bold'), fg = 'royal blue', bg = 'light gray', command = topScores)
topscoresButton.place(x=280,y=500)

exitButton = Button(window, text = 'Exit Game', width = 30, font = ('fixedsys', '30', 'bold'), fg = 'royal blue', bg = 'light gray', command = exitGame)
exitButton.place(x=280,y=600)

# Enter name frame
enterName_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
entryName = Entry(enterName_frame, width=40, font=50)
entryName.place(x=100,y=300)
nameLabel = Label(enterName_frame, text = 'Enter your name:', width = 20, font = ('fixedsys', '34'), fg = 'royal blue', bg = 'lightskyblue')
nameLabel.place(x=0,y=100)
nameButton = Button(enterName_frame, text = 'Start New Game!', width = 20, font = ('fixedsys', '24'), fg = 'royal blue', bg = 'light gray', command = playerName)
nameButton.place(x=100,y=500)

# Top Scores frame
topScores_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
scoreText = Text(topScores_frame, width = 100, font = ('fixedsys', 34), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0)
scoreText.place(x=60,y=100)
returnButton = Button(topScores_frame, text = 'Return to Main Menu', width = 30, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'light gray', command = returnBack)

# New game frame
newGame_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
dayText = Text(newGame_frame, width = 100, font = ('fixedsys', 34), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0)
dayText.place(x=40,y=15)
    
characterButton = Button(newGame_frame, text = 'View Character', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = playerStats)
characterButton.place(x=250,y=150)

mapButton = Button(newGame_frame, text = 'View Map', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = printMap)
mapButton.place(x=250,y=240)

moveButton = Button(newGame_frame, text = 'Move', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = move)
moveButton.place(x=250,y=330)

restButton = Button(newGame_frame, text = 'Rest', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = rest)
restButton.place(x=250,y=420)

saveButton = Button(newGame_frame, text = 'Save Game', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = saveData)
saveButton.place(x=250,y=510)

exitButton = Button(newGame_frame, text = 'Exit Game', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = exitGame)
exitButton.place(x=250,y=600)

senseButton = Button(newGame_frame, text = 'Sense Orb', width = 30, font = ('fixedsys', '26'), fg = 'royal blue', bg = 'light gray', command = senseOrb)
senseButton.place(x=250,y=420)

# View character frame
viewChar_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
statsText = Text(viewChar_frame, width=25, height=10, font = ('fixedsys', '40'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0) 
statsText.place(x=250,y=150)

# View map frame
viewMap_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
mapText = Text(viewMap_frame, width=40, height=20, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0) 
mapText.place(x=250,y=100)
backButton = Button(viewMap_frame, text = 'Back', width = 10, font = ('fixedsys', '20'), fg = 'royal blue', bg = 'light gray', command = goBack_map)
backButton.place(x=10,y=20)

# Move frame
move_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)

# Rest frame
rest_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)

# Sense orb frame
sense_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
senseText = Text(sense_frame, width=50, height=40, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0) 
senseText.place(x=150,y=100)

# Combat menu frame and buttons 
combat_frame = Frame(window, bg='lightskyblue', width = 1920, height = 1080)
combatText = Text(combat_frame, width = 100, font = ('fixedsys', '35'), fg = 'royal blue', bg = 'lightskyblue', borderwidth=0)
combatText.place(x=40,y=50)
attackButton = Button(newGame_frame, text = 'Attack', width = 8, font = ('fixedsys', '38'), fg = 'royal blue', bg = 'light gray', command = attack)
runButton = Button(newGame_frame, text = 'Run', width = 8, font = ('fixedsys', '38'), fg = 'royal blue', bg = 'light gray', command = run)
nextButton = Button(combat_frame, text = 'Next', width = 8, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = nextMove)
mainmenuButton = Button(combat_frame, text = 'Return to Main Menu', width = 30, font = ('fixedsys', '25'), fg = 'royal blue', bg = 'light gray', command = returnMainMenu)
continueButton = Button(combat_frame, text = 'Continue', width = 8, font = ('fixedsys', '30'), fg = 'royal blue', bg = 'light gray', command = continueFight)

window.mainloop()