"""
Levels/scenes for rpg game

Please accompany with a .png image with the same name

2 - unreachable area
1 - difficult terrain
0 - normal ground
"""
import random

def t ():
    # Trees
    # Returns t1, t2, t3, or t4 (random)
    return 't' + str(random.randint(1, 4))

scene1 = {
    'movement': [[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2]],
    'objects': [[t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()],
                [t(), t(), None, None, None, None, None, None, None, None, None, None, None, t(), t()]],
    'tiles': [['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g'],
              ['g', 'g', 'g', 'g', 'gr', 'r', 'r', 'r', 'r', 'r', 'rg', 'g', 'g', 'g', 'g']]
}
