"""
Author: Trevor Stalnaker
File: itemselect.py

A variable length version of the inventory HUD that can be used
to prompt the user for item selections
"""

import pygame
from polybius.graphics import Drawable, AbstractGraphic
from .itemblock import ItemBlock


class ItemSelect(AbstractGraphic):

    def __init__(self, pos, items, dimensions=(700,50)):
        """Initializes the item selection interface"""
        super().__init__(pos)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._items = items
        self._position.x += (9-(len(items))) * ((self._width//9)/2)
        self._selected = 0
        self._blocks = []
        self._itemSelected = None
        for x in range(len(items)):
            if x < len(self._items):
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=self._items[x],
                              selected=x==self._selected)
            else:
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=None,
                              selected=x==self._selected)
            self._blocks.append(i)

        # Used purely for centering purposes
        self._image = pygame.Surface((self.getWidth(), self._height))

    def getItemSelected(self):
        """Returns the selected item"""
        return None if self._itemSelected==None else self._itemSelected.getItem()

    def handleEvent(self, event):
        """Handle events on the item selector"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self._selected = (self._selected + 1) % 9
            if event.button == 5:
                self._selected = (self._selected - 1) % 9
            if event.button == 1:
                for i, b in enumerate(self._blocks):
                    if b.getCollideRect().collidepoint(event.pos):
                        self._selected = i
                        self._itemSelected = self._blocks[self._selected]
                    

    def update(self):
        """Update the display of the item selector"""
        self._blocks = []
        for x in range(len(self._items)):
            if x < len(self._items):
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=self._items[x],
                              selected=x==self._selected)
            else:
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=None,
                              selected=x==self._selected)
            self._blocks.append(i)
        
    def draw(self, screen):
        """Draw the item selector to the screen"""
        # Draw the background
        for block in self._blocks:
            block.draw(screen)

    def getItemBlocks(self):
        """Returns the number of blocks in the selection"""
        return len(self._blocks)

    def getWidth(self):
        """Returns the width of the item selector"""
        return sum([x.getWidth() for x in self._blocks])

    def resetItems(self,newItems):
        """"Resets the items in the item selector and resets the selected item to None"""
        self._items = newItems
        self._itemSelected = None
        self._image = pygame.Surface((self.getWidth(), self._height))
        self.updateCentering()
