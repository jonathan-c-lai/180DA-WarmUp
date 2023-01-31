# Took python tutorial https://realpython.com/pygame-a-primer/#basic-game-design that professor
# and TA linked in Lab 3, and then modified it so that I have an RPS game instead
# I did not actually use that much of the code in tutorial, but it was the inspiration
# used code here to learn how to sprite click detection https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# used code here to learn how to display text https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# used code here to learn how to use in-game time https://stackoverflow.com/questions/18839039/how-to-wait-some-time-in-pygame

import pygame
import random
from pygame.locals import (
    RLEACCEL
)

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
        return 'CPU Wins'
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
large_font = pygame.font.Font('fonts/arial.ttf', 48)
text = font.render('Select Your Option', True, (140, 150, 100), (255,255,255))
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/5)
cpu_text = large_font.render(' ', True, (140, 150, 100), (255,255,255))
cpu_textRect = cpu_text.get_rect()
cpu_textRect.center = (SCREEN_WIDTH/2, (4*SCREEN_HEIGHT)/5)

# flags for game state, if option select is true then player should select
Option_select = True

# flag to tell game to keep going or stop when False
running = True
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
            
            CPU_input = str(random.randint(1,3))

            # update text on the screen
            text = font.render('You picked ' + convert(user_input), True, (140, 150, 100), (255,255,255))
            cpu_text = large_font.render('CPU picked ' + convert(CPU_input) + ' ... ' + rps_result(user_input,CPU_input), True, (140, 150, 100), (255,255,255))
            cpu_textRect = cpu_text.get_rect()
            cpu_textRect.center = (SCREEN_WIDTH/2, (4*SCREEN_HEIGHT)/5)

            print('\n\n')
            print("You picked ", convert(user_input), ' and the CPU picked ', convert(CPU_input))
            print('Result: ', rps_result(user_input,CPU_input))

        if event.type == pygame.QUIT:
            running = False

    # fill the background with white
    screen.fill((255, 255, 255))

    # draw three rps sprites
    screen.blit(rock.surf, (rock_x, rock_y))
    screen.blit(paper.surf, (paper_x, paper_y))
    screen.blit(scissors.surf, (scissors_x, scissors_y))

    # draw message text
    screen.blit(text, textRect)
    screen.blit(cpu_text, cpu_textRect)

    # actually draw display, without this, nothing will be drawn
    pygame.display.flip()

pygame.quit()