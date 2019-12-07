"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for hedgehog. It contains the individual
stats that effects the NPCs performance.

We also incorporate the image of the hedgehog as well as the
rows needed from the sprite sheet to create the appropriate animations.
"""

from .npc import NPC
from modules.animated import Animated

# stats needed for the hedgehog
AGGRESSION   = (0,2)
SPEED        = (12,18)
ENDURANCE    = (6,10)
ATTACK_SPEED = (1,2)
STRENGTH     = 10

class Hedgehog(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the hedgehog.
        We also specify the rows that we need for the animations.
        """
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


