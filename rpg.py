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
from send2trash import *

import pygame
from pygame.locals import *
from textrect import render_textrect, TextRectException

import levels
from monsters import *
from characters import *

# All options for game
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WINDOWCAPTION = 'RPG Game'
WINDOWICON = 'icon.png'

FPS = 30

#Start with a clean save until proper system is implemented
send2trash('save.bak')
send2trash('save.dat')
send2trash('save.dir')
SAVE = shelve.open('save', writeback=True)


# Colour      R    G    B   (A)
# ==============================
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
BLUE       = (  0,   0, 255)
LIGHTGREEN = (137, 199,  94)


def main ():
    global DISPLAY, FPSCLOCK, BASICFONT, PIXELFONT, PIXELFONTLARGE

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
    PIXELFONTLARGE = pygame.font.Font('pixelart.ttf', 32)

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

        tile_img = pygame.image.load(tile('titlescreen')).convert_alpha()
        DISPLAY.blit(tile_img, adj_tile_to_pix(3, 1, 30, 0))
        render_text_centered(6, 1, PIXELFONT, 'The', LIGHTGREEN)
        render_text_centered(6.5, 2, PIXELFONTLARGE, 'Dungeons', LIGHTGREEN)
        render_text_centered(7, 3, PIXELFONT, 'Of', LIGHTGREEN)
        render_text_centered(8, 4, PIXELFONTLARGE, 'Feymere', LIGHTGREEN)
        
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
            #SAVE['PC'] = Cleric()
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 7, 6, 7) and pressed[0]: # Wizard
            #SAVE['PC'] = Wizard()
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 9, 6, 9) and pressed[0]: # Ranger
            #SAVE['PC'] = Ranger()
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 11, 6, 11) and pressed[0]: # Fighter
            #SAVE['PC'] = Fighter()
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 13, 6, 13) and pressed[0]: # Rogue
            #SAVE['PC'] = Rogue()
            SAVE.sync()
            self.next = Introduction()

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
        text_surf = render_textrect(('STRENGTH determines your physical prowess and the bonuses you get when fighting with melee weapons.\n\n'
                                     'DEXTERITY determines your balance and manoeuvrability, and the bonuses you get when fighting with ranged or finesse weapons.\n\n'
                                     'CONSTITUTION determines your characters \'toughness\'\n\n'
                                     'INTELLIGENCE determines your overall knowledge, and is the spellcasting ability for Wizards\n\n'
                                     'WISDOM determines your insightfulness and perceptiveness, and is the spellcasting ability for Clerics and Rangers\n\n'
                                     'CHARISMA determines your characters personality and skill in social activities\n\n'), PIXELFONT, tiles_to_rect(1, 3, 13, 13), WHITE, 0)
        text_rect = text_surf.get_rect()
        text_rect.center = adj_tile_to_pix(7, 8, 20, 20)
        DISPLAY.blit(text_surf, text_rect)

class Introduction(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(5, 10, 9, 10) and pressed[0]: # Back button
            self.next = Sc1GoblinAttack()
    
    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        set_tile(5, 10, 'styled_button_left')
        set_tile(6, 10, 'button_middle')
        set_tile(7, 10, 'button_middle')
        set_tile(8, 10, 'button_middle')
        set_tile(9, 10, 'styled_button_right')
        render_text_centered(7, 10, PIXELFONT, 'Continue', WHITE)
        text_surf = render_textrect(('Bob McBobface, a noble from the city of Durin is paying you '
                                     'and your party TEN gold pieces each to escort him to the town '
                                     'of Feymere. Payment will only be delivered upon safe arrival '
                                     'at Feymere.\n\n'
                                     'You left Durin in the early hours of second day morning. The '
                                     'story begins approximately half way through the second day of '
                                     'travelling...'), PIXELFONT, tiles_to_rect(1, 1, 9, 5), WHITE, 1).convert_alpha()
        text_rect = text_surf.get_rect()
        text_rect.topleft = tile_to_pix(3, 4)
        DISPLAY.blit(text_surf, text_rect)
        

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
    # TODO: allow to exit with custom error
    SAVE.close()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
