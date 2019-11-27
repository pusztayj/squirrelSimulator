"""
Author: Trevor Stalnaker
File: inventory.py

A class modeling a heads up display for the player's inventory
"""

import pygame
from modules.drawable import Drawable
from modules.frameManager import FRAMES
from items.items import Spear
from .itemblock import ItemBlock
from graphics import TextBox

class InventoryHUD(Drawable):

    def __init__(self, pos, dimensions, player):
        super().__init__("", pos, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._player = player
        self._items = [item for item in self._player.getInventory()]
        self._selected = 0
        self._blocks = []
        for x in range(9):
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

        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._activeItem = TextBox("Item", (0,0), self._font, (255,255,255))
        self._activeItem.setPosition((self._position[0] + (self._width//2)-self._activeItem.getWidth()//2,
                                        self._position[1]-30))

        self._activeDisplayTime = .75
        self._displayTimer = self._activeDisplayTime

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            # Check if the keys 1 through 9 were pressed
            if event.key in [x for x in range(49,58)]:
                self._selected = event.key - 49
                self._displayTimer = self._activeDisplayTime
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self._selected = (self._selected + 1) % 9
                self._displayTimer = self._activeDisplayTime
            if event.button == 5:
                self._selected = (self._selected - 1) % 9
                self._displayTimer = self._activeDisplayTime
            if event.button == 1:
                for i, b in enumerate(self._blocks):
                    if b.getCollideRect().collidepoint(event.pos):
                        self._selected = i
                        self._displayTimer = self._activeDisplayTime
                    

    def update(self, ticks):
        self._items = [item for item in self._player.getInventory()]
        self._blocks = []
        for x in range(9):
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
        if self.getActiveItem() != None:
            self._activeItem.setText(self.getActiveItem().getName())
        else:
            self._activeItem.setText("")
        self._activeItem.setPosition((self._position[0] + (self._width//2)-self._activeItem.getWidth()//2,
                                        self._position[1]-30))
        self._displayTimer -= ticks

    def getActiveItem(self):
        if self._selected < len(self._items):
            return self._items[self._selected]
        else:
            return None
        
    def draw(self, screen):
        # Draw the background
        for block in self._blocks:
            block.draw(screen)
        if self._displayTimer > 0:
            self._activeItem.draw(screen)



