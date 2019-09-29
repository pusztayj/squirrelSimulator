
import pygame
from drawable import Drawable
from textbox import TextBox

class Button(Drawable):

    def __init__(self, text, position, font, color, backgroundColor,
                 height, width, borderColor=(0,0,0), borderWidth=0):
        super().__init__("", position, worldBound=False)
        self._fontColor = color
        self._font = font
        self._backgroundColor = backgroundColor
        self._text = text
        self._height = height
        self._width = width
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self.__updateButton()

    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor
        self.__updateButton()

    def setText(self, text):
        self._text = text
        self.__updateButton()

    def setFont(self, font):
        self._font = font
        self.__updateButton()

    def setFontColor(self, color):
        self._fontColor = color

    def setBorderColor(self, color):
        self._borderColor = borderColor

    def setBorderWidth(self, width):
        self._borderWidth = width
    
    def __updateButton(self):
        """Update the textbox after parameters have been changed"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)
        t = TextBox(self._text, (0,0), self._font, self._fontColor)
        y_pos = (self._height // 2) - (t.getHeight() // 2)
        x_pos = (self._width // 2) - (t.getWidth() // 2)
        t.setPosition((x_pos, y_pos))
        t.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
