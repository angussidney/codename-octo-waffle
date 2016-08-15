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

LEVELFILE = "levels.txt"


# Colour      R    G    B   (A)
# ==============================
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
BLUE      = (  0,   0, 255)
GREEN     = (  0, 255,   0)


def main ():
    global DISPLAY, FPSCLOCK, BASICFONT, PIXELFONT

    pygame.init()

    # Set up display and icons
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(WINDOWCAPTION)
    icon = pygame.image.load(WINDOWICON)
    pygame.display.set_icon(icon)
    
    # FPS
    FPSCLOCK = pygame.time.Clock()

    # Fonts
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    PIXELFONT = pygame.font.Font('pixelart.ttf', 16)

    active_scene = TitleScreen()

    DISPLAY.fill(WHITE)
    pygame.draw.rect(DISPLAY, BLACK, (0, 0, 600, 400))
    pygame.draw.rect(DISPLAY, WHITE, (0, 0, 40, 40))
    set_tile(1, 0, 'tile3')

    set_tile(2, 0, 'styled_button_left')
    set_tile(3, 0, 'styled_button_middle')
    set_tile(4, 0, 'styled_button_middle')
    set_tile(5, 0, 'styled_button_middle')
    set_tile(6, 0, 'styled_button_right')
    render_text_centered(4, 0, PIXELFONT, 'For the lolz', WHITE)
    
    while True: # main game loop
        active_scene.Render()
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
    
    def Render(self):
        # Render to the main display object
        raise NotImplementedError('Don\'t forget to override this in the child class!')

class TitleScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
    
    def ProcessInput(self):
        pass
        #mousex, mousey = pygame.mouse.get_pos()
        #pressed = pygame.mouse.get_pressed()

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        set_tile(5, 6, 'styled_button_left')
        set_tile(6, 6, 'styled_button_middle')
        set_tile(7, 6, 'styled_button_middle')
        set_tile(8, 6, 'styled_button_middle')
        set_tile(9, 6, 'styled_button_right')
        render_text_centered(7, 6, PIXELFONT, 'Continue', WHITE)

        set_tile(5, 8, 'styled_button_left')
        set_tile(6, 8, 'styled_button_middle')
        set_tile(7, 8, 'styled_button_middle')
        set_tile(8, 8, 'styled_button_middle')
        set_tile(9, 8, 'styled_button_right')
        render_text_centered(7, 8, PIXELFONT, 'New Game', WHITE)

        set_tile(5, 10, 'styled_button_left')
        set_tile(6, 10, 'styled_button_middle')
        set_tile(7, 10, 'styled_button_middle')
        set_tile(8, 10, 'styled_button_middle')
        set_tile(9, 10, 'styled_button_right')
        render_text_centered(7, 10, PIXELFONT, 'About', WHITE)

        set_tile(5, 12, 'styled_button_left')
        set_tile(6, 12, 'styled_button_middle')
        set_tile(7, 12, 'styled_button_middle')
        set_tile(8, 12, 'styled_button_middle')
        set_tile(9, 12, 'styled_button_right')
        render_text_centered(7, 12, PIXELFONT, 'Credits', WHITE)

def tile (tile_name):
    # Returns the filepath of a tile
    return os.path.join('tiles', tile_name + '.png')

def set_tile (x, y, tile_img):
    # Sets the tile at (x, y) to the designated image
    tile_img = pygame.image.load(tile(tile_img)).convert_alpha()
    DISPLAY.blit(tile_img, tile_to_pix(x, y))

def pix_to_tile (x, y):
    # Converts pixel co-ordinates (x, y) to tile co-ordinates (x, y)
    # E.g. (36, 90) => (0, 2)
    # x+1 and y+1 so that (40, 40) is (1, 1) not (0, 0) 
    return (math.floor((x + 1) / 40), math.floor((y + 1) / 40))

def tile_to_pix (x, y):
    # Takes a tile co-ordinate and returns the top-left pixel co-ordinate
    # E.g. (1, 2) => (40, 80)
    return (x * 40, y * 40)

def render_text_centered (x, y, font, text, color):
    # Renders text centered on the given tile co-ordinate
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    pixel_coords = tile_to_pix(x, y)
    adj_pixel_coords = (pixel_coords[0] + 20, pixel_coords[1] + 20)
    text_rect.center = adj_pixel_coords
    DISPLAY.blit(text_surf, text_rect)
    

if __name__ == '__main__':
    main()
