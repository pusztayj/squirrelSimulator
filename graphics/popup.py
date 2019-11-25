"""
Author: Trevor Stalnaker, justin Pusztay
File: popup.py
"""

from .textbox import TextBox
from modules import Drawable
import pygame
from .guiUtils import makeMultiLineTextBox

class Popup(Drawable):

    def __init__(self, text, position, font,
                 color=(0,0,0), backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderWidth=1, margin=2,multiLine = False):
        super().__init__("", position, worldBound=False)
        if multiLine == True:
            self._textbox = makeMultiLineTextBox(text,(0,0),font,color,backgroundColor)
        else:
            self._textbox = TextBox(text, (0,0), font, color)
        self._backgroundColor = backgroundColor
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._width = self._textbox.getWidth() + (margin * 2)
        self._height = self._textbox.getHeight() + (margin * 2)
        self.__updatePopup()

    def __updatePopup(self):
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)
        y_pos = (self._height // 2) - (self._textbox.getHeight() // 2)
        x_pos = (self._width // 2) - (self._textbox.getWidth() // 2)
        self._textbox.setPosition((x_pos, y_pos))
        self._textbox.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
