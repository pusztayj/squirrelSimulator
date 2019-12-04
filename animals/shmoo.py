"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for shmoo. It contains the individual
stats that effects the NPCs performance.
"""

from .npc import NPC
from modules.animated import Animated

# stats needed for the shmoo
AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (6,8)
STRENGTH     = 100

class Shmoo(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the shmoo.
        """
        NPC.__init__(self, name, "shmoo.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

        self._maxVelocity = 40

        # Specify which rows contain which animations
        self._standRow = 0
        self._walkRow = 0
        self._forwardRow = 0
        self._backwardRow = 0
        
        # Specify how many frames for each animation
        self._standFrames    = 1
        self._walkFrames     = 1
        self._forwardFrames  = 1
        self._backwardFrames = 1

        
