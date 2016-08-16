# Base classes for all monsters in the game

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
