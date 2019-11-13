
import pygame
from modules.drawable import Drawable
from .itemblock import ItemBlock

class threeXthreeInventory(Drawable):

    def __init__(self, pos, dimensions, entity):
        super().__init__("", pos, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._entity = entity
        self._items = [item for item in self._entity.getInventory()]
        self._blocks = []
        for x in range(3):
            for y in range(3):
                if x+y < len(self._items):
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=self._items[x])
                else:
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*(self._height//3))+self._position[1]),
                              (self._width//3,self._height//3),item=None)
                self._blocks.append(i)

    def handleEvent(self, event):
        pass

    def update(self):
        self._items = [item for item in self._entity.getInventory()]
        self._blocks = []
        for x in range(3):
            for y in range(3):
                if x+y < len(self._items):
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*self._height//3)+self._position[1]),
                              (self._width//3,self._height//3),item=self._items[x])
                else:
                    i = ItemBlock((self._position[0]+(x*(self._width//3)),
                               (y*self._height)+self._position[1]),
                              (self._width//3,self._height//3),item=None)
                self._blocks.append(i)

    def getActiveItem(self):
        if self._selected < len(self._items):
            return self._items[self._selected]
        else:
            return None
        
    def draw(self, screen):
        # Draw the background
        for block in self._blocks:
            block.draw(screen)
