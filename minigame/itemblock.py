"""
Author: Trevor Stalnaker
File: itemblock.py

A class that can be used as a building block for the various
inventory themed classes or used on its own as an item frame
"""

import pygame
from polybius.graphics import Drawable, ProgressBar
from polybius.managers import CONSTANTS

class ItemBlock(Drawable):

    def __init__(self, pos, dimensions=(77,50), item=None,
                 selected=False, showDurability=True,
                 backgroundColor=(100,100,100)):
        """Initializes an item block"""
        super().__init__("", pos, worldBound = False)
        self._item = item
        self._width = dimensions[0]
        self._height = dimensions[1]

        self._borderColor = (0,0,0)
        self._selectedBorder = (150,150,150)
        self._backgroundColor = backgroundColor
        self._borderWidth = 1

        self._transparency = 200

        self._selected = selected

        self._showDurability = showDurability
        if self._item != None:
            self.initializeDurabilityDisplay()

        self.updateBlock()

    def initializeDurabilityDisplay(self):
        length = 3 * self._width // 4
        x_pos = (self._width//2) - (length + 2)//2
        y_pos = self._height - 10
        maxStat = self._item.getAttribute("maxDurability")
        actStat = self._item.getAttribute("durability")
        height = 4
        self._durBar = ProgressBar((x_pos, y_pos), length, maxStat, actStat,
                                   height=height)
        
    def setItem(self, item):
        """Sets the item in the item block"""
        self._item = item
        if self._item != None:
            self.initializeDurabilityDisplay()
        self.updateBlock()

    def getItem(self):
        """Returns the item linked to the block"""
        return self._item

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.getCollideRect().collidepoint(pygame.mouse.get_pos()):
                return self.getItem()

    def updateBlock(self):
        """Update the display of the item block"""
        surfBack = pygame.Surface((self._width, self._height))
        if self._selected:
            surfBack.fill(self._selectedBorder)
        else:
            surfBack.fill(self._borderColor)
        surfBack.set_alpha(self._transparency)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)
        surf.set_alpha(self._transparency)

        if self._item != None:
            image = self._item.getImage()
            centerX = self._width//2 - self._item.getWidth()//2
            centerY = self._height//2 - self._item.getHeight()//2
            surf.blit(image,(centerX,centerY))

            itemHasDurability = self._item.getAttribute("type") != "potion"
            if self._showDurability and itemHasDurability:
                self._durBar.setProgress(self._item.getAttribute("durability"))
                self._durBar.draw(surf)
        
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
