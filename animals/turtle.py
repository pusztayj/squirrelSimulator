"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for turtle. It contains the individual
stats that effects the NPCs performance.
"""

from .npc import NPC

# stats needed for the turtle
AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 10

class Turtle(NPC):

    def __init__(self, name="", pos=(0,0), worldBound=True):
        """
        We set the appropriate stats to create the NPC for the turtle.
        """
        NPC.__init__(self,name,"turtle.png", pos,AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)
        self.setWorldBound(worldBound)
