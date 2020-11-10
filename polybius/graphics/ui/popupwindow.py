"""
Author: Trevor Stalnaker
File: popupwindow.py

A class that models and manages a pop up notification window
"""

import pygame
from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.graphics.utils.window import Window
from polybius.graphics.components.textbox import TextBox
from polybius.graphics.components.button import Button
from polybius.graphics.components.multilinetextbox import MultiLineTextBox

class PopupWindow(AbstractGraphic, Window):

    def __init__(self, text, position, dimensions, font, fontColor,
                 backgroundColor, buttonColor, buttonDimensions, buttonFont,
                 buttonFontColor, buttontext="OK", buttonBorderWidth=1,
                 buttonBorderColor=(0,0,0), borderWidth=0, borderColor=(0,0,0)):
        """Initializes the widget with a variety of parameters"""
        AbstractGraphic.__init__(self, position)
        Window.__init__(self)
        self._height = dimensions[1]
        self._width = dimensions[0]
        self._text = text
        self._font = font
        self._fontColor = fontColor
        self._backgroundColor = backgroundColor
        self._borderWidth = borderWidth
        self._borderColor = borderColor

        self._offset = position

        self._confirmed = None

        self._image = pygame.Surface((self._width, self._height))

        # Create the textbox
        self._t = MultiLineTextBox(self._text, (0,0), self._font,
                                       self._fontColor, self._backgroundColor)
        self._t.center(surface=self, cen_point=(1/2,1/4))
        
        # Create the Okay button
        self._b = Button(buttontext, (0,0), buttonFont, buttonFontColor,
                         buttonColor,buttonDimensions[1],
                         buttonDimensions[0],buttonBorderColor, buttonBorderWidth)
        self._b.center(surface=self, cen_point=(1/2,3/4))

        self.updateGraphic()

    def setText(self, text):
        """Sets the text of the pop up and centers the new text"""
        alreadyFormatted = "\n" in text
        self._t.setText(text)
        if not alreadyFormatted:
            self.formatText()
        self._t.center(surface=self, cen_point=(1/2,1/4))
        self.updateGraphic()

    def confirm(self):
        """Closes the window and sets the confirmed flag to true"""
        self.close()
        self._confirmed = True

    def getConfirmed(self):
        """Returns the boolean confirmation and resets it to None"""
        con = self._confirmed
        self._confirmed = None
        return con

    def handleEvent(self, event):
        """Handles events on the pop up window"""
        self._offset = self._position
        self._b.handleEvent(event,self.confirm,offset=self._offset)
        self.updateGraphic()

    def internalUpdate(self, surf):
        """Updates the attributes of the pop up window"""      
        self._t.draw(surf)
        self._b.draw(surf)

    def formatText(self):
        availableWidth = self._width * 0.8
        words = self._t.getText().split()
        retString = ""
        pixelCount = 0
        for i, w in enumerate(words):
          if pixelCount + self.getPixelWidth(w) > availableWidth:
             retString += "\n" + w
             pixelCount = self.getPixelWidth(w)
          else:
             if i != 0:
                retString += " "
             retString += w
             pixelCount += self.getPixelWidth(w + " ")
        self._t.setText(retString)

    def getPixelWidth(self, text):
        font = self._font
        width, height = font.size(text)
        return width
        
        
