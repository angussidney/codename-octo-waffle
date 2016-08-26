class Character(object):
    proficiency_bonus = 2
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.proficiencies['skills'][skill][0] == True:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.proficiencies['skills'][skill][1])

class Fighter(Character):
    def __init__(self):
        Character.__init__(self)
    level = 1
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
    hp = 10 + score_to_bonus('con')
    ac = 18 # Chain mail fixed + shield
