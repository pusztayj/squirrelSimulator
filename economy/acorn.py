"""
Author: Trevor Stalnaker
File: acorn.py

A class modeling acorns
"""

from modules.drawable import Drawable
import random

class Acorn(Drawable):

    def __init__(self, pos, worldBound=True):
        super().__init__("acorn.png", pos, worldBound=worldBound)
        self._collected = False
        self._lifespan = random.randint(45,120)

    def collected(self):
        self._collected = True

    def isCollected(self):
        return self._collected

    def update(self, ticks):
        if self._lifespan < 0:
            self.collected()
        self._lifespan -= ticks
        
