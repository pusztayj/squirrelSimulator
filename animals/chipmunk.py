
from .npc import NPC

AGGRESSION   = (0,2)
SPEED        = (12,18)
ENDURANCE    = (6,10)
STRENGTH     = 8 

class Chipmunk(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "new_chipmunk.png", pos,
                     AGGRESSION, SPEED, ENDURANCE,STRENGTH)

        self._maxVelocity = 60

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
