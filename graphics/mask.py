"""
Author: Trevor Stalnaker
File: mask.py
"""

import pygame
from modules.drawable import Drawable

class Mask(Drawable):

    def __init__(self, position, dimensions, color, alpha, worldBound=False):
        super().__init__("", position, worldBound=worldBound)
        self._image = pygame.Surface(dimensions)
        self._image.fill(color)
        self._image.set_alpha(0)
        self._alpha = alpha

    def setAlpha(self, alpha):
        self._alpha = alpha
        self._image.set_alpha(alpha)

    def getAlpha(self):
        return self._alpha

    def setColor(self, color):
        self._image.fill(color)
