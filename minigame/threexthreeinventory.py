"""
Author: Trevor Stalnaker
File: threexthreeinventory.py

The inventory HUD displayed as a 3x3 grid
"""

import pygame
from polybius.graphics import Drawable
from .itemblock import ItemBlock

class threeXthreeInventory(Drawable):

    def __init__(self, pos, dimensions, entity):
        """Initializes the 3 x 3 inventory block"""
        super().__init__("", pos, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._entity = entity
        self._items = [item for item in self._entity.getInventory()]
        self._blocks = []
        count = 0
        for y in range(3):
            for x in range(3):
                if count < len(self._items):
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=self._items[count])
                else:
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=None)
                self._blocks.append(i)
                count += 1

    def handleEvent(self, event):
        """Handles events on the 3 x 3 inventory"""
        pass  ## Complete if ever needed

    def update(self):
        """Updates the display of the 3x3 inventory"""
        self._items = [item for item in self._entity.getInventory()]
        self._blocks = []
        count = 0
        for y in range(3):
            for x in range(3):
                if count < len(self._items):
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=self._items[count])
                else:
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=None)
                self._blocks.append(i)
                count += 1

    def getActiveItem(self):
        """Returns the active item if there is one"""
        if self._selected < len(self._items):
            return self._items[self._selected]
        else:
            return None
        
    def draw(self, screen):
        """Draws the 3x3 inventory to the screen"""
        for block in self._blocks:
            block.draw(screen)
