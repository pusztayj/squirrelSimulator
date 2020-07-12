"""
Author: Trevor Stalnaker
File: button.py

A class that creates and manages a button object
"""

import pygame
from graphics.textgraphic import TextGraphic
from graphics.textbox import TextBox

class Button(TextGraphic):

    def __init__(self, text, position, font, fontColor, backgroundColor,
                 height, width, borderColor=(0,0,0), borderWidth=0,
                 antialias=True):
        """Initializes the widget with a variety of parameters"""
        
        super().__init__(position, text, font, fontColor, antialias)
        
        self._width = width
        self._height = height
        
        self._backgroundColor = backgroundColor
        self._borderColor = borderColor
        self._borderWidth = borderWidth

        # Current button colors
        self._currentFontColor = fontColor
        self._currentBackgroundColor = backgroundColor

        self.updateGraphic()

    def setBackgroundColor(self, backgroundColor):
        """Sets the button's background color"""
        self._backgroundColor = backgroundColor
        self.updateGraphic()

    def setBorderColor(self, color):
        """Sets the button's border color"""
        self._borderColor = borderColor
        self.updateGraphic()

    def setBorderWidth(self, width):
        """Set's the button's border width"""
        self._borderWidth = width
        self.updateGraphic()

    def buttonPressed(self):
        """Updates the button styling when button is pressed"""
        self._currentFontColor = self.shiftRGBValues(self._fontColor,
                                                     (40,40,40))
        self._currentBackgroundColor = self.shiftRGBValues(self._backgroundColor,
                                                            (20,20,20))
        self.updateGraphic()

    def setToDefaultStyling(self):
        """Updates the button to its default style"""
        self._currentBackgroundColor = self._backgroundColor
        self._currentFontColor = self._fontColor
        self.updateGraphic()

    def handleEvent(self, event, func, *args, offset=(0,0)):
        """Handles events on the button"""
        rect = self.getCollideRect()
        rect = rect.move(offset[0],offset[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if rect.collidepoint(event.pos):
                self.buttonPressed()
                func(*args)
        elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                self.setToDefaultStyling()
        elif rect.collidepoint(pygame.mouse.get_pos()):
            self.setHover()
        else:
            self.setToDefaultStyling()
                
    def setHover(self):
        """Updates the button's sytling when the mouse hovers over the button"""
        self._currentBackgroundColor = self.shiftRGBValues(self._backgroundColor,
                                                           (-40,-40,-40))
        self.updateGraphic()

    def internalUpdate(self, surf):
        """Update the button after parameters have been changed"""

        # Use the current background color
        surf.fill(self._currentBackgroundColor)

        # Create and draw the internal textbox
        t = TextBox(self._text, (0,0), self._font,
                    self._currentFontColor, self._antialias)
        t.center(surf)
        t.draw(surf)

