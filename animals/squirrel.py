"""
@authors: Trevor Stalnaker, Justin Pusztay

This file contains the class for squirrel. It contains the individual
stats that effects the NPCs performance.
"""

from .animal import Animal
from modules.animated import Animated
from modules.vector2D import Vector2
import pygame

class Squirrel(Animal, Animated):

    def __init__(self, name="", pos=(0,0)):
        """
        We set the appropriate stats to create the NPC for the squirrel.
        """
        Animal.__init__(self, name)
        Animated.__init__(self, "new_squirrel.png", pos)

        self._nFrames = 4
        

   

    
        

    
