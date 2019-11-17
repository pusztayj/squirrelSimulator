
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,2)
SPEED        = (12,18)
ENDURANCE    = (6,10)
ATTACK_SPEED = (1,2)
STRENGTH     = 7

class HedgeHog(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "tempHedgeHog.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)


