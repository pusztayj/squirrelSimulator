"""
Author: Trevor Stalnaker
File Name: drawable.py
Date: 22 September 2019
Project 2

A textbox class that inherits from the Drawable class
"""

from drawable import Drawable

class TextBox(Drawable):

    def __init__(self, text, position, font, color):
        """
        Initializes a textbox object with text, position, font, and
        font color
        """
        super().__init__("", position, worldBound=False)
        self._fontColor = color
        self._font = font
        self._text = text
        self.__updateTextBox()

    def setText(self, text):
        """Sets the text of a textbox"""
        self._text = text
        self.__updateTextBox()

    def setFont(self, font):
        """Sets the font of the textbox"""
        self._font = font
        self.__updateTextBox()

    def setFontColor(self, fontColor):
        """Sets the font color of the textbox"""
        self._fontColor = fontColor
        self.__updateTextBox()

    def getText(self, text):
        """Returns the current text of the textbox"""
        return self._text

    def getFont(self, font):
        """Returns the current font of the textbox"""
        return self._font

    def getFontColor(self):
        """Returns the current font color of the textbox"""
        return self._fontColor

    def __updateTextBox(self):
        """Update the textbox after parameters have been changed"""
        self._image = self._font.render(self._text, False, self._fontColor)
