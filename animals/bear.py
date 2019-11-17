
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (6,8)
STRENGTH = 45

class Bear(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "tempBear.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

