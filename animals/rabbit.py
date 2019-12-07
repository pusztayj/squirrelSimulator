"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for rabbit. It contains the individual
stats that effects the NPCs performance.

We also incorporate the image of the rabbit as well as the
rows needed from the sprite sheet to create the appropriate animations.
"""

from .npc import NPC

# stats needed for the rabbit
AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 14

class Rabbit(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the rabbit.
        We also specify the rows that we need for the animations.
        """
        NPC.__init__(self, name, "new_rabbit.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

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
