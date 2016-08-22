####################
# Todo: credit pixel art font (cc-by-sa)
# credit textrect function http://www.pygame.org/pcr/text_rect/index.php
# also: https://pymotw.com/2/shelve/
####################

import math
import random
import sys
import os
import traceback
import shelve

import pygame
from pygame.locals import *
from textrect import render_textrect, TextRectException

import levels
import monsters

# All options for game
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WINDOWCAPTION = 'RPG Game'
WINDOWICON = 'icon.png'

FPS = 30

LEVELS = 'levels.txt'
SAVE = shelve.open('save', writeback=True)


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

    # DISPLAY.fill(WHITE)
    # pygame.draw.rect(DISPLAY, BLACK, (0, 0, 600, 400))
    # ^ size of game scene - 15 x 10

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        try:
            active_scene.ProcessInput()
            active_scene.Update()
            active_scene.Render()
            active_scene = active_scene.next
        except Exception: # Catch any errors and exit gracefully
            traceback.print_exc()
            terminate()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

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
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(5, 6, 9, 6) and pressed[0]: # Continue button
            self.next = CharacterSelection() # self.next = Continue()
        if mouse_between_tiles(5, 8, 9, 8) and pressed[0]: # New Game button
            self.next = CharacterSelection()
        if mouse_between_tiles(5, 10, 9, 10) and pressed[0]: # About button
            self.next = About()
        if mouse_between_tiles(5, 12, 9, 12) and pressed[0]: # Exit button
            terminate()

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        set_tile(5, 6, 'styled_button_left')
        set_tile(6, 6, 'button_middle')
        set_tile(7, 6, 'button_middle')
        set_tile(8, 6, 'button_middle')
        set_tile(9, 6, 'styled_button_right')
        render_text_centered(7, 6, PIXELFONT, 'Continue', WHITE)

        set_tile(5, 8, 'styled_button_left')
        set_tile(6, 8, 'button_middle')
        set_tile(7, 8, 'button_middle')
        set_tile(8, 8, 'button_middle')
        set_tile(9, 8, 'styled_button_right')
        render_text_centered(7, 8, PIXELFONT, 'New Game', WHITE)

        set_tile(5, 10, 'styled_button_left')
        set_tile(6, 10, 'button_middle')
        set_tile(7, 10, 'button_middle')
        set_tile(8, 10, 'button_middle')
        set_tile(9, 10, 'styled_button_right')
        render_text_centered(7, 10, PIXELFONT, 'About', WHITE)

        set_tile(5, 12, 'styled_button_left')
        set_tile(6, 12, 'button_middle')
        set_tile(7, 12, 'button_middle')
        set_tile(8, 12, 'button_middle')
        set_tile(9, 12, 'styled_button_right')
        render_text_centered(7, 12, PIXELFONT, 'Exit', WHITE)

class About(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(6, 1, 8, 1) and pressed[0]: # Back button
            self.next = TitleScreen()

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        set_tile(6, 1, 'styled_button_left')
        set_tile(7, 1, 'button_middle')
        set_tile(8, 1, 'styled_button_right')
        render_text_centered(7, 1, PIXELFONT, 'Back', WHITE)
        ## TODO: REPLACE WITH SOMETHING MORE ELEGANT AND MULTILINE STRING (brackets then standard string no comma)
        text_surf = render_textrect('\'The Dungeons of Feymere\' is an RPG game written by angussidney. Some of the game is based on a simplified version of the rules contained in the DnD 5e SRD.\n\nThe source code of this program is released under the MIT license. See LICENSE.txt for details.', PIXELFONT, tiles_to_rect(2, 3, 12, 13), WHITE, 0)
        text_rect = text_surf.get_rect()
        text_rect.center = adj_tile_to_pix(7, 8, 20, 20)
        DISPLAY.blit(text_surf, text_rect)

class CharacterSelection(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.y = None
        self.text = None

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        # Need help?
        if mouse_between_tiles(1, 3, 5, 3) and pressed[0]:
            self.next = CharacterHelp()
            pass
        # Determine which character is currently being looked at
        if mouse_between_tiles(1, 5, 6, 5): # Cleric
            self.y = 5
            self.text = ("Cleric\n"
                         "stuff\n"
                         "goes\n"
                         "here\n")
        if mouse_between_tiles(1, 7, 6, 7): # Wizard
            self.y = 7
            self.text = ("Wizard\n"
                         "stuff\n"
                         "goes\n"
                         "here\n")
        if mouse_between_tiles(1, 9, 6, 9): # Ranger
            self.y = 9
            self.text = ("Ranger\n"
                         "stuff\n"
                         "goes\n"
                         "here\n")
        if mouse_between_tiles(1, 11, 6, 11): # Fighter
            self.y = 11
            self.text = ("Fighter\n"
                         "stuff\n"
                         "goes\n"
                         "here\n")
        if mouse_between_tiles(1, 13, 6, 13): # Rogue
            self.y = 13
            self.text = ("Rogue\n"
                         "stuff\n"
                         "goes\n"
                         "here\n")
        # Determine if a character has been selected
        if mouse_between_tiles(1, 5, 6, 5) and pressed[0]: # Cleric
            SAVE['PC'] = 'Cleric'
            SAVE.sync()
            #self.next =
        if mouse_between_tiles(1, 7, 6, 7) and pressed[0]: # Wizard
            SAVE['PC'] = 'Wizard'
            SAVE.sync()
            #self.next =
        if mouse_between_tiles(1, 9, 6, 9) and pressed[0]: # Ranger
            SAVE['PC'] = 'Ranger'
            SAVE.sync()
            #self.next =
        if mouse_between_tiles(1, 11, 6, 11) and pressed[0]: # Fighter
            SAVE['PC'] = 'Fighter'
            SAVE.sync()
            #self.next =
        if mouse_between_tiles(1, 13, 6, 13) and pressed[0]: # Rogue
            SAVE['PC'] = 'Rogue'
            SAVE.sync()
            #self.next =

    def Update(self):
        pass
    
    def Render(self):
        DISPLAY.fill(BLACK)
        for i in range(15):
            set_tile(6, i, 'vertical_divider')
        # Instructions
        text_surf = render_textrect(('Choose a character from the options below. '
                                     'Hover for more info.'), PIXELFONT, tiles_to_rect(1, 0, 5, 2), WHITE, 1)
        text_rect = text_surf.get_rect()
        text_rect.center = adj_tile_to_pix(3, 2, 20, 0)
        DISPLAY.blit(text_surf, text_rect)
        # Help me choose button
        set_tile(1, 3, 'styled_button_left')
        set_tile(2, 3, 'button_middle')
        set_tile(3, 3, 'button_middle')
        set_tile(4, 3, 'button_middle')
        set_tile(5, 3, 'styled_button_right')
        render_text_centered(3, 3, PIXELFONT, 'Help me choose', WHITE)
        # Show information for current character
        try:
            set_tile(1, self.y, 'end_button_left')
            set_tile(2, self.y, 'button_middle')
            set_tile(3, self.y, 'button_middle')
            set_tile(4, self.y, 'button_middle')
            set_tile(5, self.y, 'button_middle')
            set_tile(6, self.y, 'arrow_button_right')
            text_surf = render_textrect(self.text, PIXELFONT, tiles_to_rect(7, 2, 13, 13), WHITE, 0)
            text_rect = text_surf.get_rect()
            text_rect.center = adj_tile_to_pix(10, 7, 20, 20)
            DISPLAY.blit(text_surf, text_rect)
        except Exception: # Do nothing if no character is selected yet
            pass
        render_text_centered(3, 5, PIXELFONT, 'Cleric', WHITE)
        render_text_centered(3, 7, PIXELFONT, 'Wizard', WHITE)
        render_text_centered(3, 9, PIXELFONT, 'Ranger', WHITE)
        render_text_centered(3, 11, PIXELFONT, 'Fighter', WHITE)
        render_text_centered(3, 13, PIXELFONT, 'Rogue', WHITE)

class CharacterHelp(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(6, 1, 8, 1) and pressed[0]: # Back button
            self.next = CharacterSelection()

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        set_tile(6, 1, 'styled_button_left')
        set_tile(7, 1, 'button_middle')
        set_tile(8, 1, 'styled_button_right')
        render_text_centered(7, 1, PIXELFONT, 'Back', WHITE)

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

def adj_tile_to_pix (x, y, adj_x, adj_y):
    return ((x * 40) + adj_x, (y * 40) + adj_y)

def tiles_to_rect (x1, y1, x2, y2):
    top_left = tile_to_pix(x1, y1)
    bottom_right = adj_tile_to_pix(x2, y2, 39, 39)
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]
    return pygame.Rect(x1, y1, width, height)

def render_text_centered (x, y, font, text, color):
    # Renders text centered on the given tile co-ordinate
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = adj_tile_to_pix(x, y, 20, 20)
    DISPLAY.blit(text_surf, text_rect)

def mouse_between_tiles (x1, y1, x2, y2):
    # Tests if the mouse is anywhere between any of the
    mousex, mousey = pygame.mouse.get_pos()
    top_left = tile_to_pix(x1, y1)
    bottom_right = adj_tile_to_pix(x2, y2, 39, 39)
    if mousex >= top_left[0] and mousex <= bottom_right[0] \
       and mousey >= top_left[1] and mousey <= bottom_right[1]:
        return True

def terminate():
    # Exits pygame and closes the window properly
    SAVE.close()
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

if __name__ == '__main__':
    main()
