
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

        # Specify which rows contain which animations
        self._standRow = 0
        self._walkRow = 1
        self._forwardRow = 2
        self._backwardRow = 3
        
        # Specify how many frames for each animation
        self._standFrames    = 1
        self._walkFrames     = 3
        self._forwardFrames  = 3
        self._backwardFrames = 3
