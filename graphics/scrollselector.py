"""
Author: Trevor Stalnaker
File: scrollselector.py
"""

import pygame
from modules.drawable import Drawable
from .scrollbox import ScrollBox
from .button import Button
from .mysurface import MySurface

class ScrollSelector(Drawable):

    def __init__(self, position, dimensions, selections, backgroundColor):
        super().__init__("", position, worldBound=False)
        self._dimensions = dimensions
        self._selections = selections
        self._backgroundColor = backgroundColor
        internalSurface = self.makeDisplay()
        self._scrollBox = ScrollBox(position, dimensions, internalSurface)
        self.update()

    def makeDisplay(self):
        surf = pygame.Surface((self._dimensions[0] * 3, self._dimensions[1] * 3))
        selectorWidth = self._dimensions[1] // len(self._selections)
        font = pygame.font.SysFont("Times New Roman", 16)        
        ypos = 0
        for sel in self._selections:
            Button(sel["text"], (0,ypos), font,(255,255,255),self._backgroundColor,
                   selectorWidth, self._dimensions[0]).draw(surf)
            ypos += selectorWidth
        return MySurface(surf)

    def handleEvent(self, event):
        self._scrollBox.move(event)
        self.update()

    def update(self):
        self._image = self._scrollBox.getImage()
        

    
