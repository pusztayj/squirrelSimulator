
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 25 

class Cow(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "cow.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)
