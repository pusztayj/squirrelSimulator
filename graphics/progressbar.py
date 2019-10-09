"""
Author: Trevor Stalnaker
File: progressbar.py

A GUI widget that can be used to model progress bars or health bars
"""

import pygame
from modules.drawable import Drawable

class ProgressBar(Drawable):

    def __init__(self, position, length, maxStat, actStat, borderWidth=1,
                 borderColor=(0,0,0), backgroundColor=(120,120,120),
                 barColor=(255,0,0)):
        super().__init__("", position, worldBound=False)
        self._length = length
        self._height = 10
        self._maxStat = maxStat
        self._actStat = actStat
        self._borderWidth = borderWidth
        self._borderColor = borderColor
        self._backgroundColor = backgroundColor
        self._barColor = barColor
        self.updateBar()

    def setProgress(self, actStat):
        self._actStat = actStat
        self._updateBar()

    def changeProgress(self, amount):
        if 0 < self._actStat + amount <= self._maxStat: 
            self._actStat += amount
            self.updateBar()

    def updateBar(self):
        surfBack = pygame.Surface((self._length+(self._borderWidth*2),
                                   self._height+(self._borderWidth*2)))
        surfBack.fill(self._borderColor)
        barBack = pygame.Surface((self._length,self._height))
        barBack.fill(self._backgroundColor)
        surfBack.blit(barBack, (self._borderWidth, self._borderWidth))
        barLength = round((self._actStat / self._maxStat) * self._length)
        bar = pygame.Surface((barLength,self._height))
        bar.fill(self._barColor)
        surfBack.blit(bar, (self._borderWidth, self._borderWidth))
        self._image = surfBack
