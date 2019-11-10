
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (6,8)
STRENGTH     = 12

class Rabbit(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)

        Animated.__init__(self, "tempRabbit.png", pos)
