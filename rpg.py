####################
# Todo: credit pixel art font (cc-by-sa)
####################

import math
import random
import sys
import os

import pygame
from pygame.locals import *

import levels

# All options for game
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WINDOWCAPTION = "RPG Game"
WINDOWICON = "icon.png"

FONTSIZE = 20

LEVELFILE = "levels.txt"


# Colour      R    G    B   (A)
# ==============================
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
BLUE      = (  0,   0, 255)
GREEN     = (  0, 255,   0)


def main ():
    global DISPLAY, FPSCLOCK, BASICFONT

    pygame.init()

    # Set up display and icons
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(WINDOWCAPTION)
    icon = pygame.image.load(WINDOWICON)
    pygame.display.set_icon(icon)
    
    # FPS
    FPSCLOCK = pygame.time.Clock()

    # Fonts
    BASICFONT = pygame.font.Font('freesansbold.ttf', FONTSIZE)

    DISPLAY.fill(WHITE)
    pygame.draw.rect(DISPLAY, RED, (0, 0, 600, 400))
    pygame.draw.rect(DISPLAY, BLACK, (0, 0, 40, 40))
    set_tile(1, 0, os.path.join('tiles', 'tile2.png'))
    
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

class Character(object):
    proficiency_bonus = 2
    scores = {
        'strength': 10,
        'dex': 10,
        'con': 10,
        'intelligence': 10,
        'wis': 10,
        'cha': 10
    }
    skills = {
        # 'skill': (is_proficient, base score),
        'athletics': (False, 'strength'),
        'acrobatics': (False, 'dex'),
        'sleight_of_hand': (False, 'dex'),
        'stealth': (False, 'dex'),
        'arcana': (False, 'intelligence'),
        'history': (False, 'intelligence'),
        'investigation': (False, 'intelligence'),
        'nature': (False, 'intelligence'),
        'religion': (False, 'intelligence'),
        'animal_handling': (False, 'wis'),
        'insight': (False, 'wis'),
        'medicine': (False, 'wis'),
        'perception': (False, 'wis'),
        'survival': (False, 'wis'),
        'deception': (False, 'cha'),
        'intimidation': (False, 'cha'),
        'performance': (False, 'cha'),
        'persuasion': (False, 'cha')
    }
    saving_throws = {
        'strength': False,
        'dex': False,
        'con': False,
        'intelligence': False,
        'wis': False,
        'cha': False
    }
    def score_to_bonus (self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus (self, skill):
        if self.skills[skill][0] == True:
            return self.score_to_bonus(self.skills[skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.skills[skill][1])

class Goblin(object):
    ac = 15
    hp = 7
    speed = 30
    xp = 50
    languages = ['Common', 'Goblin']
    scores = {
        'strength': 8,
        'dex': 14,
        'con': 10,
        'intelligence': 10,
        'wis': 8,
        'cha': 8
    }

class SceneBase(object):
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events):
        # Recieves all events that have happened since last frame
        raise NotImplementedError('Don\'t forget to override this in the child class!')
    
    def Update(self):
        # Game logic goes here
        raise NotImplementedError('Don\'t forget to override this in the child class!')
    
    def Render(self, screen):
        # Render to the main display object
        raise NotImplementedError('Don\'t forget to override this in the child class!')

class TitleScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
    
    def ProcessInput(self):
        pass

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        

def set_tile (x, y, image):
    tile_img = pygame.image.load(image).convert_alpha()
    DISPLAY.blit(tile_img, tile_to_pixel_coords(x, y))

def pixel_to_tile_coords (x, y):
    # Converts pixel co-ordinates (x, y) to tile co-ordinates (x, y)
    # E.g. (36, 90) => (0, 2)
    # x+1 and y+1 so that (40, 40) is (1, 1) not (0, 0) 
    return (math.floor((x + 1) / 40), math.floor((y + 1) / 40))

def tile_to_pixel_coords (x, y):
    # Takes a tile co-ordinate and returns the top-left pixel co-ordinate
    # E.g. (1, 2) => (40, 80)
    return (x * 40, y * 40)

if __name__ == '__main__':
    main()
