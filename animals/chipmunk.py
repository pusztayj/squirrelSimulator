
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,2)
HEALTH       = (10,15)
SPEED        = (12,18)
ENDURANCE    = (6,10)
DAMAGE       = (4,6)
ATTACK_SPEED = (1,2)
DEFENSE      = (5,7)

class Chipmunk(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
        Animated.__init__(self, "tempChipmunk.png", pos)
