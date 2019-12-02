"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for cow. It contains the individual
stats that effects the NPCs performance.
"""

from .npc import NPC
from modules.animated import Animated

# stats needed for the cow
AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 25 

class Cow(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the cow.
        """
        NPC.__init__(self, name, "cow.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)
