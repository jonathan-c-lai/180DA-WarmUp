# Took python tutorial https://realpython.com/pygame-a-primer/#basic-game-design that professor
# and TA linked in Lab 3, and then modified it so that I have an RPS game instead
# I did not actually use that much of the code in tutorial, but it was the inspiration
# used code here to learn how to sprite click detection https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# used code here to learn how to display text https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# used code here to learn how to use in-game time https://stackoverflow.com/questions/18839039/how-to-wait-some-time-in-pygame
# used code that the professor/TA posted for MQTT, modified completely to have it work for RPS game and sending message on decision that each player picked

# These resources above were used to create RPS game that works for 2P remotely using MQTT,
# the two players can just pick their choice of RPS by clicking a sprite on the screen and then their
# selection gets transmitted by MQTT, the players then receive the msg that opponent broadcasts
# and locally computes the result of winner / score counter (no central server)

import paho.mqtt.client as mqtt
import pygame
from pygame.locals import (
    RLEACCEL
)

# MQTT
player = 1
# flags
player1_received = False
player2_received = False
# player's moves
player1_move = 0
player2_move = 0

# game player 1
# for MQTT:
# both subscribe to same thing 
# start in select mode; upon clicking one of the options go into waiting
    # (should display waiting at the bottom)
# then if the other person also selected, reset both flags back to normal
    # and display result
# then after 3 seconds go back to select

# callback definitions
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180/team1/rps_pygame", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
# The default message callback.
def on_message(client, userdata, message):
    global counter
    global player1_received
    global player2_received
    global player1_move
    global player2_move

    #print('Received message: "' + str(message.payload) + '" on topic "' +
    #        message.topic + '" with QoS ' + str(message.qos))
    print('\n')
    split_msg = str(message.payload)

    if (split_msg[2] == str(1)):
        player1_received = True
        player1_move = split_msg[3]

    elif(split_msg[2] == str(2)):
        player2_received = True
        player2_move = split_msg[3]
        
# RPS game logic from my own rps_cli game
# 1 is Rock
# 2 is Paper
# 3 is Scissors
ROCK = '1'
PAPER = '2'
SCISSORS = '3'

def convert(val):
    returnval = ''
    if (val == ROCK):
        returnval = 'Rock'
    elif (val == PAPER):
        returnval = 'Paper'
    elif (val == SCISSORS):
        returnval = 'Scissors'
    return returnval

def rps_result(p1, p2):
    # rp, rs, pr, ps, sr, sp
    # 12, 13, 21, 23, 31, 32
    if (p1 == p2):
        return 'Tie'
    elif ((p1 == ROCK and p2 == PAPER) or (p1 == PAPER and p2 == SCISSORS) or (p1 == SCISSORS and p2 == ROCK)):
        return 'Opponent Wins'
    elif ((p1 == ROCK and p2 == SCISSORS) or (p1 == PAPER and p2 == ROCK) or (p1 == SCISSORS and p2 == PAPER)):
        return 'You Win!'

# screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# constants for setting where on the screen I want the RPS sprites
rock_x = 2*SCREEN_WIDTH/10
rock_y = SCREEN_HEIGHT/3
paper_x = 4.3*SCREEN_WIDTH/10
paper_y = SCREEN_HEIGHT/3
scissors_x = 6.5*SCREEN_WIDTH/10
scissors_y = SCREEN_HEIGHT/3

rock_image = pygame.image.load("RPS_Sprites/rock.png")
paper_image = pygame.image.load("RPS_Sprites/paper.jpg")
scissors_image = pygame.image.load("RPS_Sprites/scissors.png")

# set up sprites for the three rps
# defined rps by extending pygame.sprite.Sprite
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super(Rock, self).__init__()
        self.surf = rock_image.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(rock_x, rock_y))
class Paper(pygame.sprite.Sprite):
    def __init__(self):
        super(Paper, self).__init__()
        self.surf = paper_image.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(paper_x, paper_y))
class Scissors(pygame.sprite.Sprite):
    def __init__(self):
        super(Scissors, self).__init__()
        self.surf = scissors_image.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(scissors_x, scissors_y))

pygame.init()

# set up drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# initialize rps sprites
rock = Rock()
paper = Paper()
scissors = Scissors()

# put all sprites in group to see if they got clicked on
all_sprites = pygame.sprite.Group()
all_sprites.add(rock)
all_sprites.add(paper)
all_sprites.add(scissors)

# set up font for displaying results and instructions
font = pygame.font.Font('fonts/arial.ttf', 48)
large_font = pygame.font.Font('fonts/arial.ttf', 45)
text = font.render('Select Your Option', True, (140, 150, 100), (255,255,255))
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/5)
cpu_text = large_font.render(' ', True, (140, 150, 100), (255,255,255))
cpu_textRect = cpu_text.get_rect()
cpu_textRect.center = (SCREEN_WIDTH/2, (4*SCREEN_HEIGHT)/5)
score_text = font.render('P1 Score: 0', True, (140, 150, 100), (255,255,255))
score_textRect = score_text.get_rect()
score_textRect.topleft = (20, 20)

# flag to tell game to keep going or stop when False
running = True

# game time to track when to prompt user for option again
last_time = pygame.time.get_ticks()
go_back_to_options_tick = 3000

# score to keep track score
score = 0

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

while running:
    # check for event that user close game or click on sprite
    for event in pygame.event.get():
        # if user clicked on a sprite, do the calculation for what the CPU picked and then display who won
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            user_input = 0
            # if clicked rock:
            if rock.rect.collidepoint(pos):
                user_input = ROCK
            elif paper.rect.collidepoint(pos):
                user_input = PAPER
            elif scissors.rect.collidepoint(pos):
                user_input = SCISSORS
            
            client.publish("ece180/team1/rps_pygame", str(player)+str(user_input), qos=1)
            print('Published message: ', str(player)+str(user_input))

        if event.type == pygame.QUIT:
            running = False

    # if both players made selection, then set time before returning to selection
    # also reset selection
    # also print result
    if (player1_received and player2_received):
        player1_received = False
        player2_received = False

        last_time = pygame.time.get_ticks()

        # update text on the screen
        text = font.render('You picked ' + convert(user_input), True, (140, 150, 100), (255,255,255))
        cpu_text = large_font.render('They picked ' + convert(player2_move) + ' ... ' + rps_result(user_input,player2_move), True, (140, 150, 100), (255,255,255))
        cpu_textRect = cpu_text.get_rect()
        cpu_textRect.center = (SCREEN_WIDTH/2, (4*SCREEN_HEIGHT)/5)

        print('\n\n')
        print("You picked ", convert(user_input), ' and the they picked ', convert(player2_move))
        print('Result: ', rps_result(user_input,player2_move))

        if (rps_result(user_input,player2_move) == "You Win!"):
            score += 1

        score_text = font.render('P1 Score: ' + str(score), True, (140, 150, 100), (255,255,255))
    elif (player1_received):
        text = font.render('You picked ' + convert(user_input), True, (140, 150, 100), (255,255,255))
        cpu_text = large_font.render('Waiting for opponent ... ', True, (140, 150, 100), (255,255,255))
        cpu_textRect = cpu_text.get_rect()
        cpu_textRect.center = (SCREEN_WIDTH/2, (4*SCREEN_HEIGHT)/5)

    # if enough time passed, change text to prompt user again
    if (pygame.time.get_ticks() - last_time > go_back_to_options_tick):
        text = font.render('Select Your Option', True, (140, 150, 100), (255,255,255))
        cpu_text = large_font.render(' ', True, (140, 150, 100), (255,255,255))
        cpu_textRect = cpu_text.get_rect()
    

    # fill the background with white
    screen.fill((255, 255, 255))

    # draw three rps sprites
    screen.blit(rock.surf, (rock_x, rock_y))
    screen.blit(paper.surf, (paper_x, paper_y))
    screen.blit(scissors.surf, (scissors_x, scissors_y))

    # draw message text
    screen.blit(text, textRect)
    screen.blit(cpu_text, cpu_textRect)
    screen.blit(score_text, score_textRect)

    # actually draw display, without this, nothing will be drawn
    pygame.display.flip()

pygame.quit()