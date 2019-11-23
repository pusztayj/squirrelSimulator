
import pygame
from modules.drawable import Drawable
from modules.frameManager import FRAMES
from items.items import Spear
from .itemblock import ItemBlock


class ItemSelect(Drawable):

    def __init__(self, pos, items, dimensions=(700,50)):
        super().__init__("", pos, worldBound=False)
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

    def getItemSelected(self):
        return self._itemSelected

    def handleEvent(self, event):
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
        # Draw the background
        for block in self._blocks:
            block.draw(screen)

    def getItemBlocks(self):
        return len(self._blocks)

    def getWidth(self):
        return sum([x.getWidth() for x in self._blocks])

    def resetItems(self,newItems):
        self._items = newItems
        self._itemSelected = None
