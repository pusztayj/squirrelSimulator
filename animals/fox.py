
from .npc import NPC

AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 15

class Fox(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self,name, "new_fox.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)
        

        self._nFrames = 1
