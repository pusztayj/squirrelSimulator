
from npc import NPC
from animated import Animated

AGGRESSION   = (0,1)
HEALTH       = (14,18)
SPEED        = (18,24)
ENDURANCE    = (6,10)
DAMAGE       = (6,8)
ATTACK_SPEED = (1,2)
DEFENSE      = (3,5)

class Deer(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
        Animated.__init__(self, "tempDeer.png", pos)
