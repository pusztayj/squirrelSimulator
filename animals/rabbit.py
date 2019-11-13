
from .npc import NPC

AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (6,8)
STRENGTH     = 12

class Rabbit(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "new_rabbit.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)

        self._maxVelocity = 100

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
