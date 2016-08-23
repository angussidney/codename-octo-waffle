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
    def score_to_bonus(self, score):
        return math.floor((self.scores[score] - 10) / 2)
    def calculate_bonus(self, skill):
        if self.skills[skill][0] == True:
            return self.score_to_bonus(self.skills[skill][1]) + self.proficiency_bonus
        else:
            return self.score_to_bonus(self.skills[skill][1])
