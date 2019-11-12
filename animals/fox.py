
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 15

class Fox(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self,name, AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)
        Animated.__init__(self, "new_fox.png", pos)

        self._nFrames = 1
