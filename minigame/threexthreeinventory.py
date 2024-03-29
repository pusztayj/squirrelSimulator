"""
Author: Trevor Stalnaker
File: threexthreeinventory.py

The inventory HUD displayed as a 3x3 grid
"""

import pygame
from polybius.graphics import Drawable
from .itemblock import ItemBlock
from polybius.managers import CONSTANTS

class threeXthreeInventory(Drawable):

    def __init__(self, pos, dimensions, entity):
        """Initializes the 3 x 3 inventory block"""
        super().__init__("", pos, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._entity = entity

        # Determine how to color item blocks
        player = CONSTANTS.get("player")
        self._colorKey = {}
        if entity in player.getPack():
            self._toggleItemColors = True
            self._colorKey[player] = CONSTANTS.get("playerItemHighlight")
            colors = [CONSTANTS.get("firstPackMemberItemHighlight"),
                      CONSTANTS.get("secondPackMemberItemHighlight")]
            for animal in player.getPack().getTrueMembers():
                if animal != player:
                    newColor = colors[0]
                    self._colorKey[animal] = newColor
                    colors.remove(newColor)
        else:
            self._toggleItemColors = False
            for animal in entity.getPack().getTrueMembers():
                self._colorKey[animal] = CONSTANTS.get("defaultItemHighlight")
            

        self.createItemBlocks()
        

    def createItemBlocks(self):
        self._items = [item for item in self._entity.getInventory()]
        self._blocks = []
        count = 0
        for y in range(3):
            for x in range(3):
                if count < len(self._items):
                    item = self._items[count]
                    itemOwner = item.getAttribute("owner")
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=item,
                                  backgroundColor=self._colorKey[itemOwner])
                else:
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=None)
                self._blocks.append(i)
                count += 1

    def handleEvent(self, event):
        """Handles events on the 3 x 3 inventory"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for block in self._blocks:
                if block.getCollideRect().collidepoint(pygame.mouse.get_pos()):
                    return block.getItem()

    def update(self):
        """Updates the display of the 3x3 inventory"""
        self.createItemBlocks()

    def getActiveItem(self):
        """Returns the active item if there is one"""
        if self._selected < len(self._items):
            return self._items[self._selected]
        else:
            return None

    def getEntity(self):
        return self._entity
        
    def draw(self, screen):
        """Draws the 3x3 inventory to the screen"""
        for block in self._blocks:
            block.draw(screen)
