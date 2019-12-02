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
STRENGTH     = 50

class Shmoo(NPC):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the shmoo.
        """
        NPC.__init__(self, name, "shmoo.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

        
