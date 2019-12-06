"""
Author: Trevor Stalnaker
File: acorn.py

A class modeling acorns. It also checks whether or not an acorn has been
collected and handles the draw and update methods for having it appear
in the main world. 
"""

from modules.drawable import Drawable
import random

class Acorn(Drawable):

    def __init__(self, pos, worldBound=True):
        """Initialize an acorn object"""
        super().__init__("acorn.png", pos, worldBound=worldBound)
        self._collected = False
        self._lifespan = random.randint(45,120)

    def collected(self):
        """Sets collected to true"""
        self._collected = True

    def isCollected(self):
        """Returns a boolean representing if the acorn has been collected"""
        return self._collected

    def update(self, ticks):
        """Update the acorn to determine if it should be despawned"""
        if self._lifespan < 0:
            self.collected()
        self._lifespan -= ticks
        
