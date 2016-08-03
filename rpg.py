import math
import random
import sys
import pygame
from pygame.locals import *

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
        # 'skill': (is_proficient, base score)
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

if __name__ == '__main__':
    main()
