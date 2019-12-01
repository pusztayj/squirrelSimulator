
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (0,2)
SPEED        = (12,18)
ENDURANCE    = (6,10)
ATTACK_SPEED = (1,2)
STRENGTH     = 7

class Hedgehog(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "new_hedgehog.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

        self._maxVelocity = 60

        # Specify which rows contain which animations
        self._standRow = 0
        self._walkRow = 1
        self._forwardRow = 2
        self._backwardRow = 3
        
        # Specify how many frames for each animation
        self._standFrames    = 1
        self._walkFrames     = 4
        self._forwardFrames  = 4
        self._backwardFrames = 4


