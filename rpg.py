####################
# Todo: credit pixel art font (cc-by-sa)
# credit textrect function http://www.pygame.org/pcr/text_rect/index.php
# also: https://pymotw.com/2/shelve/
# other section for weapons
#
# Names
# Ben Shadowsoul (fighter)
# Culhwch Blacktroll (ranger)
# Ceithin Jadeflail (wizard)
# Conal Trickybones (rogue)
# Edana Earthlydrum (cleric)
# Kei Frightfulwood (player)
####################

import math
import random
import sys
import os
import traceback
import time
import shelve
from operator import attrgetter, itemgetter
from send2trash import *

import pygame
from pygame.locals import *
from textrect import render_textrect, TextRectException

from levels import *

# All options for game
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WINDOWCAPTION = 'The Dungeons of Feymere'
WINDOWICON = 'icon.png'

FPS = 30

MUSIC = 'overworld'

#Start with a clean save until proper system is implemented
try:
    send2trash('save.bak')
    send2trash('save.dat')
    send2trash('save.dir')
except Exception:
    print('Error: A save file could not be found. Which is good, since it was going to be deleted anyway :)')
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

    # Background music
    background_music = pygame.mixer.music.load(sound(MUSIC))
    pygame.mixer.music.play(-1, 0.0)
    mute = False

    active_scene = TitleScreen()

    # DISPLAY.fill(WHITE)
    # pygame.draw.rect(DISPLAY, BLACK, (0, 0, 600, 400))
    # ^ size of game scene - 15 x 10

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP and event.key == K_m:
                if mute == False:
                    pygame.mixer.music.set_volume(0.0)
                    mute = True
                elif mute == True:
                    pygame.mixer.music.set_volume(1.0)
                    mute = False
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

### ---------- ###
###   SCENES   ###
### ---------- ###

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
        set_tile(6, 6, 'button_middle_green')
        set_tile(7, 6, 'button_middle_green')
        set_tile(8, 6, 'button_middle_green')
        set_tile(9, 6, 'styled_button_right')
        render_text_centered(7, 6, PIXELFONT, 'Continue', WHITE)

        set_tile(5, 8, 'styled_button_left')
        set_tile(6, 8, 'button_middle_green')
        set_tile(7, 8, 'button_middle_green')
        set_tile(8, 8, 'button_middle_green')
        set_tile(9, 8, 'styled_button_right')
        render_text_centered(7, 8, PIXELFONT, 'New Game', WHITE)

        set_tile(5, 10, 'styled_button_left')
        set_tile(6, 10, 'button_middle_green')
        set_tile(7, 10, 'button_middle_green')
        set_tile(8, 10, 'button_middle_green')
        set_tile(9, 10, 'styled_button_right')
        render_text_centered(7, 10, PIXELFONT, 'About', WHITE)

        set_tile(5, 12, 'styled_button_left')
        set_tile(6, 12, 'button_middle_green')
        set_tile(7, 12, 'button_middle_green')
        set_tile(8, 12, 'button_middle_green')
        set_tile(9, 12, 'styled_button_right')
        render_text_centered(7, 12, PIXELFONT, 'Exit', WHITE)

        render_text_centered(7, 14, PIXELFONT, 'Press M at any time to mute', WHITE)

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
        set_tile(7, 1, 'button_middle_green')
        set_tile(8, 1, 'styled_button_right')
        render_text_centered(7, 1, PIXELFONT, 'Back', WHITE)
        ## TODO: REPLACE WITH SOMETHING MORE ELEGANT AND MULTILINE STRING (brackets then standard string no comma)
        text_surf = render_textrect(('\'The Dungeons of Feymere\' is an RPG game written by angussidney. '
                                     'Some of the game is based on a simplified version of the rules '
                                     'contained in the DnD 5e SRD.\n\n'
                                     'The source code of this program is released under the MIT license. '
                                     'See LICENSE.txt for details.\n\n'
                                     'Overworld by Kevin MacLeod\n'
                                     'incompetech.com\n'
                                     'Licensed under CC BY 3.0'), PIXELFONT, tiles_to_rect(2, 3, 12, 13), WHITE, 0)
        text_rect = text_surf.get_rect()
        text_rect.center = adj_tile_to_pix(7, 8, 20, 20)
        DISPLAY.blit(text_surf, text_rect)

class CharacterSelection(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.y = None
        self.text = None
        self.character_sprite = None

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        # Need help?
        if mouse_between_tiles(1, 3, 5, 3) and pressed[0]:
            self.next = CharacterHelp()
            pass
        # Determine which character is currently being looked at
        if mouse_between_tiles(1, 5, 6, 5): # Cleric
            self.y = 5
            self.text = ('Kei Frightfulwood\n'
                         'Cleric Lv 1\n\n'
                         'Strength 14\n'
                         'Dexterity 8\n'
                         'Constitution 13\n'
                         'Intelligence 10\n'
                         'Wisdom 16\n'
                         'Charisma 12\n\n'
                         'Mainly a healer and undead specialist')
            self.character_sprite = 'cleric'
        if mouse_between_tiles(1, 7, 6, 7): # Wizard
            self.y = 7
            self.text = ('Kei Frightfulwood\n'
                         'Wizard Lv 1\n\n'
                         'Strength 8\n'
                         'Dexterity 14\n'
                         'Constitution 13\n'
                         'Intelligence 16\n'
                         'Wisdom 12\n'
                         'Charisma 10\n\n'
                         'Master of the arcane arts')
            self.character_sprite = 'wizard'
        if mouse_between_tiles(1, 9, 6, 9): # Ranger
            self.y = 9
            self.text = ('Kei Frightfulwood\n'
                         'Ranger Lv 1\n\n'
                         'Strength 13\n'
                         'Dexterity 16\n'
                         'Constitution 12\n'
                         'Intelligence 10\n'
                         'Wisdom 14\n'
                         'Charisma 8\n\n'
                         'Great with nature, proficient at dual-weilding')
            self.character_sprite = 'ranger'
        if mouse_between_tiles(1, 11, 6, 11): # Fighter
            self.y = 11
            self.text = ('Kei Frightfulwood\n'
                         'Fighter Lv 1\n\n'
                         'Strength 16\n'
                         'Dexterity 13\n'
                         'Constitution 14\n'
                         'Intelligence 8\n'
                         'Wisdom 12\n'
                         'Charisma 10\n\n'
                         'All round tough guy')
            self.character_sprite = 'fighter'
        if mouse_between_tiles(1, 13, 6, 13): # Rogue
            self.y = 13
            self.text = ('Kei Frightfulwood\n'
                         'Rogue Lv 1\n\n'
                         'Strength 12\n'
                         'Dexterity 16\n'
                         'Constitution 10\n'
                         'Intelligence 14\n'
                         'Wisdom 8\n'
                         'Charisma 13\n'
                         'Master of stealth, deception and arcane trickery')
            self.character_sprite = 'rogue'
        # Determine if a character has been selected
        if mouse_between_tiles(1, 5, 6, 5) and pressed[0]: # Cleric
            SAVE['PC'] = Cleric(7, 7, True)
            SAVE['PC'].name = 'Kei Frightfulwood'
            SAVE['PC'].adress = 'You are'
            SAVE['PC'].pronoun = 'You'
            SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'] = choose_npcs(SAVE['PC'].class_name)
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 7, 6, 7) and pressed[0]: # Wizard
            SAVE['PC'] = Wizard(7, 7, True)
            SAVE['PC'].name = 'Kei Frightfulwood'
            SAVE['PC'].adress = 'You are'
            SAVE['PC'].pronoun = 'You'
            SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'] = choose_npcs(SAVE['PC'].class_name)
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 9, 6, 9) and pressed[0]: # Ranger
            SAVE['PC'] = Ranger(7, 7, True)
            SAVE['PC'].name = 'Kei Frightfulwood'
            SAVE['PC'].adress = 'You are'
            SAVE['PC'].pronoun = 'You'
            SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'] = choose_npcs(SAVE['PC'].class_name)
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 11, 6, 11) and pressed[0]: # Fighter
            SAVE['PC'] = Fighter(7, 7, True)
            SAVE['PC'].name = 'Kei Frightfulwood'
            SAVE['PC'].adress = 'You are'
            SAVE['PC'].pronoun = 'You'
            SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'] = choose_npcs(SAVE['PC'].class_name)
            SAVE.sync()
            self.next = Introduction()
        if mouse_between_tiles(1, 13, 6, 13) and pressed[0]: # Rogue
            SAVE['PC'] = Rogue(7, 7, True)
            SAVE['PC'].name = 'Kei Frightfulwood'
            SAVE['PC'].adress = 'You are'
            SAVE['PC'].pronoun = 'You'
            SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'] = choose_npcs(SAVE['PC'].class_name)
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
        set_tile(2, 3, 'button_middle_green')
        set_tile(3, 3, 'button_middle_green')
        set_tile(4, 3, 'button_middle_green')
        set_tile(5, 3, 'styled_button_right')
        render_text_centered(3, 3, PIXELFONT, 'Help me choose', WHITE)
        # Show information for current character
        try:
            set_tile(1, self.y, 'end_button_left_green')
            set_tile(2, self.y, 'button_middle_green')
            set_tile(3, self.y, 'button_middle_green')
            set_tile(4, self.y, 'button_middle_green')
            set_tile(5, self.y, 'button_middle_green')
            set_tile(6, self.y, 'arrow_button_right')
            text_surf = render_textrect(self.text, PIXELFONT, tiles_to_rect(7, 2, 13, 13), WHITE, 0)
            text_rect = text_surf.get_rect()
            text_rect.center = adj_tile_to_pix(10, 7, 20, 20)
            DISPLAY.blit(text_surf, text_rect)

            sprite_img = pygame.image.load(sprite(self.character_sprite)).convert_alpha()
            DISPLAY.blit(sprite_img, tile_to_pix(13, 1))
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
        set_tile(7, 1, 'button_middle_green')
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
        if mouse_between_tiles(5, 12, 9, 12) and pressed[0]: # Continue button
            self.next = Sc1GoblinAttack()
            time.sleep(0.2)
    
    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)
        # Summary
        text_surf = render_textrect(('Bob McBobface, a noble from the city of Durin is paying you '
                                     'and your party TEN gold pieces each to escort him to the town '
                                     'of Feymere. Payment will only be delivered upon safe arrival '
                                     'at Feymere.\n\n'
                                     'You left Durin in the early hours of second day morning. The '
                                     'story begins approximately half way through the second day of '
                                     'travelling...'), PIXELFONT, tiles_to_rect(1, 1, 9, 5), WHITE, 1).convert_alpha()
        text_rect = text_surf.get_rect()
        text_rect.topleft = tile_to_pix(3, 1)
        DISPLAY.blit(text_surf, text_rect)

        # Companions
        render_text_centered(7, 7, PIXELFONT, 'Your companions are', WHITE)
        SAVE['NPC1'].x = 3
        SAVE['NPC1'].y = 9
        SAVE['NPC2'].x = 7
        SAVE['NPC2'].y = 8
        SAVE['NPC3'].x = 11
        SAVE['NPC3'].y = 9
        SAVE['NPC1'].draw_sprite()
        SAVE['NPC2'].draw_sprite()
        SAVE['NPC3'].draw_sprite()
        render_text_centered(3, 10, PIXELFONT, SAVE['NPC1'].name, WHITE)
        render_text_centered(7, 9, PIXELFONT, SAVE['NPC2'].name, WHITE)
        render_text_centered(11, 10, PIXELFONT, SAVE['NPC3'].name, WHITE)

        # Continue
        set_tile(5, 12, 'styled_button_left')
        set_tile(6, 12, 'button_middle_green')
        set_tile(7, 12, 'button_middle_green')
        set_tile(8, 12, 'button_middle_green')
        set_tile(9, 12, 'styled_button_right')
        render_text_centered(7, 12, PIXELFONT, 'Continue', WHITE)
        
class Sc1GoblinAttack(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.round_no = 0
        self.initiative = []
        self.turn = 0
        self.turn_finished = True
        self.message_queue = ['When travelling, you were attacked by a horde of goblins! \n\nClick to view more text.']

    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(9, 11, 13, 13) and pressed[0]: # Cycle messages
            if len(self.message_queue) > 0:
                if self.message_queue[0] == 'You have lost! Better luck next time.' or \
                   self.message_queue[0] == 'Your party has won! Congratulations!': # On game over
                    self.next = GameOver()
                else:
                    del self.message_queue[0] # next message
                    time.sleep(0.2)

    def Update(self):
        # Pre-combat setup
        if self.round_no == 0:
            # Initialise combatants
            gob1 = Goblin(5, 2)
            gob2 = Goblin(6, 2)
            gob3 = Goblin(7, 2)
            gob4 = Goblin(8, 2)
            # Determine initiative
            participants = [SAVE['PC'], SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'], gob1, gob2, gob3, gob4]
            self.player_team = [SAVE['PC'], SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3']]
            self.monster_team = [gob1, gob2, gob3, gob4]
            self.non_controllable_characters = [SAVE['NPC1'], SAVE['NPC2'], SAVE['NPC3'], gob1, gob2, gob3, gob4]
            self.initiative = determine_initiative(participants)
            # Place NPCs
            SAVE['NPC1'].x = 8
            SAVE['NPC1'].y = 8
            SAVE['NPC2'].x = 7
            SAVE['NPC2'].y = 8
            SAVE['NPC3'].x = 6
            SAVE['NPC3'].y = 8
            # Determine surprise
            stealth_check = roll20(gob1.skills['stealth'])
            for character in self.player_team:
                if 10 + character.calculate_bonus('stealth') < stealth_check:
                    character.surprised = True
            self.round_no += 1

        if len(self.message_queue) == 0:
            current = self.initiative[self.turn]
            # Take their turn
            if current.is_alive == False:
                pass
            elif current.surprised:
                self.message_queue.append(current.adress + ' surprised! ' + current.pronoun + ' cannot do anything until next turn.')
                current.surprised = False
            elif current in self.non_controllable_characters:
                # NPCs and monsters
                enemy = determine_enemy(current, self.player_team, self.monster_team)
                current.attack(enemy, self)
            else:
                # Player
                enemy = determine_enemy(current, self.player_team, self.monster_team)
                current.attack(enemy, self)
            
            # Remove dead people
            for creature in self.initiative:
                if creature.hp <= 0 and creature.death_mentioned == False:
                    self.message_queue.append(creature.adress + ' dead!')
                    creature.is_alive = False
                    creature.death_mentioned = True
            # Check for win
            player_team_dead = 0
            for character in self.player_team:
                if character.is_alive == False:
                    player_team_dead += 1
            if player_team_dead == 4:
                self.message_queue.append('You have lost! Better luck next time.')
            monster_team_dead = 0
            for monster in self.monster_team:
                if monster.is_alive == False:
                    monster_team_dead += 1
            if monster_team_dead == 4:
                self.message_queue.append('Your party has won! Congratulations!')
            # When end of initiative is reached
            if self.turn == 7:
                self.turn = 0
            elif self.turn_finished:
                self.turn += 1
            SAVE.sync()
                
    def Render(self):
        # Draw scene
        draw_controls()
        try:
            draw_message(self.message_queue[0])
        except Exception:
            pass
        draw_scene(scene1)

        for creature in self.initiative:
            if creature.is_alive:
                creature.draw_sprite()

class GameOver(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        
    def ProcessInput(self):
        pressed = pygame.mouse.get_pressed()
        if mouse_between_tiles(6, 12, 8, 12) and pressed[0]: # Exit button
            terminate()

    def Update(self):
        pass

    def Render(self):
        DISPLAY.fill(BLACK)

        render_text_centered(7, 4, PIXELFONTLARGE, 'GAME OVER', WHITE)
        render_text_centered(7, 8, PIXELFONT, 'Thanks for playing!', WHITE)
        
        set_tile(6, 12, 'styled_button_left')
        set_tile(7, 12, 'button_middle_green')
        set_tile(8, 12, 'styled_button_right')
        render_text_centered(7, 12, PIXELFONT, 'Exit', WHITE)

### --------------------- ###
### CALCULATION FUNCTIONS ###
### --------------------- ###

def choose_npcs (pc):
    # Remove the PC's class from the list, shuffle it and return the first 3 NPCs
    possible_npcs = [Cleric(5, 7, True), Wizard(5, 7, True), Rogue(5, 7, True), Fighter(5, 7, True), Ranger(5, 7, True)]
    for i, npc_class in enumerate(possible_npcs):
        if npc_class.class_name == pc:
            del possible_npcs[i]
            break
    random.shuffle(possible_npcs)
    return possible_npcs[0], possible_npcs[1], possible_npcs[2]

def roll20 (bonus):
    return random.randint(1, 20) + bonus

def determine_initiative (participants):
    for i in participants:
        i.initiative = roll20(i.score_to_bonus('dex'))
    order = sorted(participants, reverse=True, key=attrgetter('initiative'))
    return order

def determine_enemy (current, player_team, monster_team):
    distances = []
    if current in player_team:
        for monster in monster_team:
            if monster.is_alive == True:
                random_modifier = random.randint(1, 3)
                distance = max(abs(monster.x - current.x) + random_modifier, abs(monster.y - current.y) + random_modifier)
                distances.append((monster, distance))
    else:
        for character in player_team:
            if character.is_alive == True:
                distance = max(abs(character.x - current.x) + 2, abs(character.y - current.y) + 2)
                distances.append((character, distance))
    new_distances = sorted(distances, key=itemgetter(1))
    return new_distances[0][0]

def occupied (x, y, creatures):
    # Check if a square is occupied
    for creature in creatures:
        if creature.x == x and creature.y == y:
            return True
    return False

### ----------------- ###
### UTILITY FUNCTIONS ###
### ----------------- ###

def tile (tile_name):
    # Returns the filepath of a tile
    return os.path.join('tiles', tile_name + '.png')

def sprite (sprite_name):
    # Returns the filepath of a tile
    return os.path.join('sprites', sprite_name + '.png')

def sound (sound_name):
    return os.path.join('sound', sound_name + '.mp3')

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
        
def terminate ():
    # Exits pygame and closes the window properly
    # TODO: allow to exit with custom error
    SAVE.close()
    pygame.quit()
    sys.exit()

### ----------------- ###
### DRAWING FUNCTIONS ###
### ----------------- ###

def draw_controls ():
    DISPLAY.fill(BLACK)
    set_tile(0, 10, 'controls_background')
    
    set_tile(1, 11, 'end_button_left_grey')
    set_tile(2, 11, 'button_middle_grey')
    set_tile(3, 11, 'end_button_right_grey')
    render_text_centered(2, 11, PIXELFONT, 'ATTACK', BLACK)
    
    if SAVE['PC'].spellcaster == True:
        set_tile(1, 13, 'end_button_left_grey')
        set_tile(2, 13, 'button_middle_grey')
        set_tile(3, 13, 'end_button_right_grey')
    else:
        set_tile(1, 13, 'end_button_left_grey')
        set_tile(2, 13, 'button_middle_grey')
        set_tile(3, 13, 'end_button_right_grey')
    render_text_centered(2, 13, PIXELFONT, 'Spells', WHITE)

    render_text_centered(4, 12, PIXELFONT, 'Controls not implemented.', BLACK)

    set_tile(5, 11, 'end_button_left_grey')
    set_tile(6, 11, 'button_middle_grey')
    set_tile(7, 11, 'end_button_right_grey')
    render_text_centered(6, 11, PIXELFONT, 'Actions', WHITE)

    set_tile(5, 13, 'end_button_left_grey')
    set_tile(6, 13, 'button_middle_grey')
    set_tile(7, 13, 'end_button_right_grey')
    render_text_centered(6, 13, PIXELFONT, 'Move', WHITE)

def draw_message (message):
    text_surf = render_textrect(message, PIXELFONT, tiles_to_rect(9, 11, 13, 13), BLACK, 1).convert_alpha()
    text_rect = text_surf.get_rect()
    text_rect.topleft = tile_to_pix(9, 11)
    DISPLAY.blit(text_surf, text_rect)

def draw_scene (scene):
    # Draw background tiles
    for y in range(len(scene['tiles'])):
        for x in range(len(scene['tiles'][y])):
            if scene['tiles'][y][x] == 'g':
                set_tile(x, y, 'grass')
            if scene['tiles'][y][x] == 'gr':
                set_tile(x, y, 'grass_road')
            if scene['tiles'][y][x] == 'rg':
                set_tile(x, y, 'road_grass')
            if scene['tiles'][y][x] == 'r':
                set_tile(x, y, 'road')

    # Draw foreground objects
    for y in range(len(scene['objects'])):
        for x in range(len(scene['objects'][y])):
            if scene['objects'][y][x] == 't1':
                set_tile(x, y, 'tree1')
            if scene['objects'][y][x] == 't2':
                set_tile(x, y, 'tree2')
            if scene['objects'][y][x] == 't3':
                set_tile(x, y, 'tree3')
            if scene['objects'][y][x] == 't4':
                set_tile(x, y, 'tree4')

    # Draw border
    pygame.draw.rect(DISPLAY, BLACK, (0, 0, 599, 399), 2)

### ------------ ###
###  CHARACTERS  ###
### ------------ ###

class Fighter(object):
    def __init__(self, x, y, is_player):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = is_player
        self.surprised = False
        self.speed_left = 6
        self.hp = 12
        self.is_alive = True
        self.death_mentioned = False
    # Meta info
    sprite = 'fighter'
    class_name = 'fighter'
    name = 'Ben Shadowsoul'
    adress = name + ' is '
    pronoun = 'They'
    spellcaster = False
    
    # DnD stuff
    level = 1
    proficiency_bonus = 2
    ac = 16
    max_hp = 12
    speed = 6
    scores = {
        'strength': 16,
        'dex': 13,
        'con': 14,
        'intelligence': 8,
        'wis': 12,
        'cha': 10
    }
    proficiencies = {
        'skills': {
            'athletics': (True, 'strength'),
            'acrobatics': (False, 'dex'),
            'sleight_of_hand': (False, 'dex'),
            'stealth': (False, 'dex'),
            'arcana': (False, 'intelligence'),
            'history': (False, 'intelligence'),
            'investigation': (False, 'intelligence'),
            'nature': (False, 'intelligence'),
            'religion': (False, 'intelligence'),
            'animal_handling': (False, 'wis'),
            'insight': (True, 'wis'),
            'medicine': (False, 'wis'),
            'perception': (True, 'wis'),
            'survival': (False, 'wis'),
            'deception': (False, 'cha'),
            'intimidation': (True, 'cha'),
            'performance': (False, 'cha'),
            'persuasion': (False, 'cha')
        },
        'saving_throws': {
            'strength': True,
            'dex': False,
            'con': True,
            'intelligence': False,
            'wis': False,
            'cha': False
        },
        'weapons': {
            'simple': True,
            'martial': True
        },
        'armor': {
            'light': True,
            'medium': True,
            'heavy': True,
            'shields': True
        }
    }
    weapons = {
        'greatsword': random.randint(1, 6) + random.randint(1, 6)
        # chain mail, martial weapon + shield, light crossbow + 20 bolts, dungeoneer's pack
    }
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])
    def saving_throw(self, ability):
        if self.proficiencies['saving_throws'][ability][0] == True:
            return self.score_to_bonus(ability) + self.proficiency_bonus
        else:
            return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def attack(self, enemy, scene_obj):
        if roll20(5) >= enemy.ac:
            damage = random.randint(1, 8) + 3
            enemy.hp -= damage
            scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his crossbow, for ' + str(damage) + ' damage!')
        else:
            scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his crossbow, but missed!')

class Cleric(object):
    def __init__(self, x, y, is_player):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = is_player
        self.surprised = False
        self.speed_left = 6
        self.hp = 9
        self.spell_slots = 2
        self.is_alive = True
        self.death_mentioned = False
    # Meta info
    sprite = 'cleric'
    class_name = 'cleric'
    name = 'Edana Earthlydrum'
    adress = name + ' is '
    pronoun = 'They'
    spellcaster = True
    
    # DnD stuff
    level = 1
    proficiency_bonus = 2
    ac = 13
    max_hp = 9
    speed = 6
    scores = {
        'strength': 14,
        'dex': 8,
        'con': 13,
        'intelligence': 10,
        'wis': 16,
        'cha': 12
    }
    proficiencies = {
        'skills': {
            'athletics': (False, 'strength'),
            'acrobatics': (False, 'dex'),
            'sleight_of_hand': (False, 'dex'),
            'stealth': (False, 'dex'),
            'arcana': (False, 'intelligence'),
            'history': (True, 'intelligence'),
            'investigation': (False, 'intelligence'),
            'nature': (False, 'intelligence'),
            'religion': (True, 'intelligence'),
            'animal_handling': (False, 'wis'),
            'insight': (True, 'wis'),
            'medicine': (True, 'wis'),
            'perception': (False, 'wis'),
            'survival': (False, 'wis'),
            'deception': (False, 'cha'),
            'intimidation': (False, 'cha'),
            'performance': (False, 'cha'),
            'persuasion': (False, 'cha')
        },
        'saving_throws': {
            'strength': False,
            'dex': False,
            'con': False,
            'intelligence': False,
            'wis': True,
            'cha': True
        },
        'weapons': {
            'simple': True,
            'martial': False
        },
        'armor': {
            'light': True,
            'medium': True,
            'heavy': False,
            'shields': True
        }
    }
    weapons = {
        'greatsword': random.randint(1, 6) + random.randint(1, 6)
        # chain mail, martial weapon + shield, light crossbow + 20 bolts, dungeoneer's pack
    }
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])
    def saving_throw(self, ability):
        if self.proficiencies['saving_throws'][ability][0] == True:
            return self.score_to_bonus(ability) + self.proficiency_bonus
        else:
            return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def attack(self, enemy, scene_obj):
        if self.spell_slots > 0 and random.randint(1, 2) == 1:
            # Guiding Bolt
            if roll20(5) >= enemy.ac:
                damage = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' cast Guiding Bolt on ' + enemy.name + ', for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to cast Guiding Bolt on ' + enemy.name + ', but failed!')
        else:
            if roll20(1) >= enemy.ac:
                damage = random.randint(1, 8) - 1
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with her crossbow, for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with her crossbow, but missed!')

class Wizard(object):
    def __init__(self, x, y, is_player):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = is_player
        self.surprised = False
        self.speed_left = 6
        self.hp = 13
        self.spell_slots = 2
        self.is_alive = True
        self.death_mentioned = False
    # Meta info
    sprite = 'wizard'
    class_name = 'wizard'
    name = 'Ceithin Jadeflail'
    adress = name + ' is '
    pronoun = 'They'
    spellcaster = True
    
    # DnD stuff
    level = 1
    proficiency_bonus = 2
    ac = 12
    max_hp = 7
    speed = 6
    scores = {
        'strength': 8,
        'dex': 14,
        'con': 13,
        'intelligence': 16,
        'wis': 12,
        'cha': 10
    }
    proficiencies = {
        'skills': {
            'athletics': (False, 'strength'),
            'acrobatics': (False, 'dex'),
            'sleight_of_hand': (False, 'dex'),
            'stealth': (False, 'dex'),
            'arcana': (True, 'intelligence'),
            'history': (True, 'intelligence'),
            'investigation': (True, 'intelligence'),
            'nature': (False, 'intelligence'),
            'religion': (False, 'intelligence'),
            'animal_handling': (False, 'wis'),
            'insight': (True, 'wis'),
            'medicine': (False, 'wis'),
            'perception': (False, 'wis'),
            'survival': (False, 'wis'),
            'deception': (False, 'cha'),
            'intimidation': (False, 'cha'),
            'performance': (False, 'cha'),
            'persuasion': (False, 'cha')
        },
        'saving_throws': {
            'strength': False,
            'dex': False,
            'con': False,
            'intelligence': True,
            'wis': True,
            'cha': False
        },
        'weapons': {
            'simple': False,
            'martial': False
        },
        'armor': {
            'light': False,
            'medium': False,
            'heavy': False,
            'shields': False
        }
    }
    weapons = {
        'greatsword': random.randint(1, 6) + random.randint(1, 6)
        # chain mail, martial weapon + shield, light crossbow + 20 bolts, dungeoneer's pack
    }
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])
    def saving_throw(self, ability):
        if self.proficiencies['saving_throws'][ability][0] == True:
            return self.score_to_bonus(ability) + self.proficiency_bonus
        else:
            return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def attack(self, enemy, scene_obj):
        if self.spell_slots > 0  and random.randint(1, 2) == 1:
            if random.randint(1, 2) == 1:
                # Magic missile
                damage = random.randint(1, 4) + random.randint(1, 4) + random.randint(1, 4) + 3
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' cast Magic Missile on ' + enemy.name + ', for ' + str(damage) + ' damage!')
            else:
                # Burning hands
                if roll20(enemy.saving_throw('dex')) <= 13:
                    damage = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                    enemy.hp -= damage
                    scene_obj.message_queue.append(self.name + ' cast Burning Hands on ' + enemy.name + ', for ' + str(damage) + ' damage!')
                else:
                    scene_obj.message_queue.append(self.name + ' tried to cast Burning Hands on ' + enemy.name + ', but failed!')
        else:
            if roll20(5) >= enemy.ac:
                damage = random.randint(1, 4) + 3
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his dagger, for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his dagger, but missed!')
                

class Rogue(object):
    def __init__(self, x, y, is_player):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = is_player
        self.surprised = False
        self.speed_left = 6
        self.hp = 8
        self.is_alive = True
        self.death_mentioned = False
    # Meta info
    sprite = 'rogue'
    class_name = 'rogue'
    name = 'Conal Trickybones'
    adress = name + ' is '
    pronoun = 'They'
    spellcaster = False
    
    # DnD stuff
    level = 1
    proficiency_bonus = 2
    ac = 14
    max_hp = 8
    speed = 6
    scores = {
        'strength': 12,
        'dex': 16,
        'con': 10,
        'intelligence': 14,
        'wis': 8,
        'cha': 13
    }
    proficiencies = {
        'skills': {
            'athletics': (False, 'strength'),
            'acrobatics': (False, 'dex'),
            'sleight_of_hand': (True, 'dex'),
            'stealth': (True, 'dex'),
            'arcana': (False, 'intelligence'),
            'history': (False, 'intelligence'),
            'investigation': (True, 'intelligence'),
            'nature': (False, 'intelligence'),
            'religion': (False, 'intelligence'),
            'animal_handling': (False, 'wis'),
            'insight': (True, 'wis'),
            'medicine': (False, 'wis'),
            'perception': (False, 'wis'),
            'survival': (False, 'wis'),
            'deception': (True, 'cha'),
            'intimidation': (True, 'cha'),
            'performance': (False, 'cha'),
            'persuasion': (False, 'cha')
        },
        'saving_throws': {
            'strength': False,
            'dex': True,
            'con': False,
            'intelligence': True,
            'wis': False,
            'cha': False
        },
        'weapons': {
            'simple': True,
            'martial': False
        },
        'armor': {
            'light': True,
            'medium': False,
            'heavy': False,
            'shields': False
        }
    }
    weapons = {
        'greatsword': random.randint(1, 6) + random.randint(1, 6)
        # chain mail, martial weapon + shield, light crossbow + 20 bolts, dungeoneer's pack
    }
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])
    def saving_throw(self, ability):
        if self.proficiencies['saving_throws'][ability][0] == True:
            return self.score_to_bonus(ability) + self.proficiency_bonus
        else:
            return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def attack(self, enemy, scene_obj):
        if random.randint(1, 2) == 1:
            # Shortbow
            if roll20(5) >= enemy.ac:
                damage = random.randint(1, 6) + 3
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his shortbow, for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his shortbow, but missed!')
        else:
            # Dagger 1
            if roll20(5) >= enemy.ac:
                damage = random.randint(1, 4) + 3
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his dagger, for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his dagger, but missed!')
            # Dagger 2
            if roll20(5) >= enemy.ac:
                damage = random.randint(1, 4) + 3
                enemy.hp -= damage
                scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his dagger, for ' + str(damage) + ' damage!')
            else:
                scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his dagger, but missed!')
            
class Ranger(object):
    def __init__(self, x, y, is_player):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = is_player
        self.surprised = False
        self.speed_left = 6
        self.hp = 11
        self.is_alive = True
        self.death_mentioned = False
    # Meta info
    sprite = 'ranger'
    class_name = 'ranger'
    name = 'Culhwch Blacktroll'
    adress = name + ' is '
    pronoun = 'They'
    spellcaster = False
    
    # DnD stuff
    level = 1
    proficiency_bonus = 2
    ac = 16
    max_hp = 11
    speed = 6
    scores = {
        'strength': 13,
        'dex': 16,
        'con': 12,
        'intelligence': 10,
        'wis': 14,
        'cha': 8
    }
    proficiencies = {
        'skills': {
            'athletics': (True, 'strength'),
            'acrobatics': (False, 'dex'),
            'sleight_of_hand': (False, 'dex'),
            'stealth': (True, 'dex'),
            'arcana': (False, 'intelligence'),
            'history': (False, 'intelligence'),
            'investigation': (True, 'intelligence'),
            'nature': (False, 'intelligence'),
            'religion': (False, 'intelligence'),
            'animal_handling': (False, 'wis'),
            'insight': (False, 'wis'),
            'medicine': (False, 'wis'),
            'perception': (True, 'wis'),
            'survival': (True, 'wis'),
            'deception': (False, 'cha'),
            'intimidation': (False, 'cha'),
            'performance': (False, 'cha'),
            'persuasion': (False, 'cha')
        },
        'saving_throws': {
            'strength': True,
            'dex': True,
            'con': False,
            'intelligence': False,
            'wis': False,
            'cha': False
        },
        'weapons': {
            'simple': True,
            'martial': True
        },
        'armor': {
            'light': True,
            'medium': True,
            'heavy': False,
            'shields': True
        }
    }
    weapons = {
        'greatsword': random.randint(1, 6) + random.randint(1, 6)
        # chain mail, martial weapon + shield, light crossbow + 20 bolts, dungeoneer's pack
    }
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])
    def saving_throw(self, ability):
        if self.proficiencies['saving_throws'][ability][0] == True:
            return self.score_to_bonus(ability) + self.proficiency_bonus
        else:
            return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def attack(self, enemy, scene_obj):
        if roll20(5) >= enemy.ac:
            damage = random.randint(1, 8) + 3
            enemy.hp -= damage
            scene_obj.message_queue.append(self.name + ' hit ' + enemy.name + ' with his longbow, for ' + str(damage) + ' damage!')
        else:
            scene_obj.message_queue.append(self.name + ' tried to hit ' + enemy.name + ' with his longbow, but missed!')

### ------------ ###
###   MONSTERS   ###
### ------------ ###

class Goblin(object):
    def __init__(self, x, y):
        self.initiative = 10
        self.x = x
        self.y = y
        self.is_player = False
        self.surprised = False
        self.speed_left = 6
        self.is_alive = True
        self.death_mentioned = False
    name = 'a goblin'
    adress = 'A goblin is'
    pronoun = 'It'
    ac = 15
    hp = 7
    speed = 6
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
    skills = {
        'stealth': 6,
    }
    sprite = 'goblin'
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def saving_throw(self, ability):
        return self.score_to_bonus(ability)
    # Methods
    def draw_sprite(self):
        img = pygame.image.load(sprite(self.sprite)).convert_alpha()
        DISPLAY.blit(img, tile_to_pix(self.x, self.y))
    def move (self, newx, newy, creatures):
        if self.x == newx or self.y == newy:
            distance = max(abs(enemy.x - self.x), abs(enemy.y - self.y))
        else:
            distance = max(abs(enemy.x - self.x) + 2, abs(enemy.y - self.y) + 2)
        if not occupied(newx, newy, creatures):
            self.x = newx
            self.y = newy
            self.speed_left -= distance
    def attack(self, enemy, scene_obj):
        ############# No melee attacks since movement AI is too hard
        #distance = max(abs(enemy.x - self.x), abs(enemy.y - self.y))
        #if enemy.x - self.x < 1:
        #    # enemy x + 1
        #elif enemyx - self.x > 1:
        #    # 
        #if distance <= 4:
        #    # Scimitar attack
        #    if roll20(4) >= enemy.ac:
        #        damage = random.randint(1, 6) + 2
        #        enemy.hp -= damage
        #        # message?
        #else:
        # Shortbow attack
        if roll20(4) >= enemy.ac:
            damage = random.randint(1, 6) + 2
            enemy.hp -= damage
            scene_obj.message_queue.append('A goblin hit ' + enemy.name + ' with their Shortbow for ' + str(damage) + ' damage!')
        else:
            scene_obj.message_queue.append('A goblin tried to hit ' + enemy.name + ' with their Shortbow, but missed!')

if __name__ == '__main__':
    main()
