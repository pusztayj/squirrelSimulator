
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,5)
HEALTH       = (25,30)
SPEED        = (15,20)
ENDURANCE    = (8,10)
DAMAGE       = (12,15)
ATTACK_SPEED = (3,4)
DEFENSE      = (6,8)

class Cow(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self,name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
        Animated.__init__(self, "cow.png", pos)
