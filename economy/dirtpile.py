"""
Author: Trevor Stalnaker
File: dirtpile.py

A class modeling buried acorn piles. Holds important data such as the
name of the pile, its capacity, and methods that regulate the inflow and
outflow of acorns.

Also handles the drawing and updating of the images of the acorn. 
"""

from polybius.graphics import Drawable
from inventory import Inventory
import pygame, random

class DirtPile(Drawable):

    def __init__(self,pos,name="Unnamed Pile",capacity=10):
        """Initialize the dirt pile"""
        super().__init__("dirtpile.png",pos)
        self._name = name
        self._acorns = 0
        self._capacity = capacity

        self._despawned = False
        self._lifespan = random.randint(120,240)

    def getName(self):
        """Returns the name of the dirt pile"""
        return self._name

    def setName(self, name):
        """Set the name of the dirt pile"""
        self._name = name

    def getCapacity(self):
        """Return the acorn capacity of the dirt pile"""
        return self._capacity

    def isEmpty(self):
        """Returns true if the pile is empty, false otherwise"""
        return self._acorns == 0

    def addAcorn(self):
        """Adds an acorn to the pile"""
        self._acorns += 1

    def removeAcorn(self):
        """Remove an acorn from the pile"""
        self._acorns -= 1

    def getAcorns(self):
        """Returns the number of acorns in the pile"""
        return self._acorns

    def setAcorns(self, acorns):
        """Sets the number of acorns in the pile"""
        self._acorns = acorns

    def handleEvent(self, event, player):
        """Handle events on the dirt pile"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                  event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                if player.getCheekCapacity() - player.getAcorns() > 0:
                    player.setAcorns(player.getAcorns() + self.getAcorns())
                    self.setAcorns(0)

    def update(self, ticks):
        """Update the dirt pile to determine if it should be despawned"""
        if self._lifespan < 0:
            self._despawned = True
        self._lifespan -= ticks
