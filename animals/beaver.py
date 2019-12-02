"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for beaver. It contains the individual
stats that effects the NPCs performance.
"""

from .npc import NPC
from modules.animated import Animated

# stats needed for the beaver
AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 20

class Beaver(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the beaver.
        """
        NPC.__init__(self, name, "beaver.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

