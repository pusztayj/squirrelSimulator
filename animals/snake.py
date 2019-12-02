"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for snake. It contains the individual
stats that effects the NPCs performance.
"""

from .npc import NPC
from modules.animated import Animated

# stats needed for the snake
AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 23

class Snake(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the snake.
        """
        NPC.__init__(self, name, "tempSnake.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)
