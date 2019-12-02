"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for bear. It contains the individual
stats that effects the NPCs performance.

We also incorporate the image of the bear as well as the
rows needed from the sprite sheet to create the appropriate animations.
"""


from .npc import NPC
from modules.animated import Animated

# stats needed for the bear
AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (6,8)
STRENGTH = 45

class Bear(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the bear.
        We also specify the rows that we need for the animations.
        """
        NPC.__init__(self, name, "new_bear.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

        self._maxVelocity = 40

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

