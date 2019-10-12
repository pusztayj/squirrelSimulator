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

    def __init__(self, position, dimensions, selections, backgroundColor,
                 borderColor=(0,0,0), borderWidth=0):
        super().__init__("", position, worldBound=False)
        self._dimensions = dimensions
        self._selections = selections
        self._buttons = []
        self._scrollBarWidth = 10
        self._backgroundColor = backgroundColor
        internalSurface = self.makeDisplay()
        self._scrollBox = ScrollBox(position, dimensions, internalSurface, borderColor, borderWidth)
        self.update()

    def makeDisplay(self):
        surf = pygame.Surface((self._dimensions[0] * 3, self._dimensions[1] * 3))
        selectorWidth = self._dimensions[1] // len(self._selections)
        font = pygame.font.SysFont("Times New Roman", 16)        
        ypos = 0
        for sel in self._selections:
            b = Button(sel["text"], (0,ypos), font,(255,255,255),self._backgroundColor,
                   selectorWidth-2, self._dimensions[0]-self._scrollBarWidth-2,
                       borderWidth=1)
            b.draw(surf)
            self._buttons.append(b)
            ypos += selectorWidth
        return MySurface(surf)

    def updateDisplay(self):
        surf = pygame.Surface((self._dimensions[0] * 3, self._dimensions[1] * 3))
        for b in self._buttons:
            b.draw(surf)
        return surf

    def handleEvent(self, event):
        self._scrollBox.move(event)
        offset = (self._position[0], self._position[1] + self._scrollBox.getOffset())
        for i,b in enumerate(self._buttons):
            if self._selections[i]["args"] != "":
                b.handleEvent(event, self._selections[i]["func"],
                              self._selections[i]["args"], offset=offset)
            else:
                b.handleEvent(event, self._selections[i]["func"], offset=offset)        
            self._scrollBox.setInternalSurface(self.updateDisplay())
            self.update()

    def update(self):
        self._scrollBox.updateScrollBox()
        self._image = self._scrollBox.getImage()
        

    
