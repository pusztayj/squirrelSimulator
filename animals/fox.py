"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for fox. It contains the individual
stats that effects the NPCs performance.

We also incorporate the image of the fox as well as the
rows needed from the sprite sheet to create the appropriate animations.
"""

from .npc import NPC

# stats needed for the fox
AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 15

class Fox(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the fox.
        We also specify the rows that we need for the animations.
        """
        NPC.__init__(self,name, "new_fox.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

        self._maxVelocity = 100
        
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
