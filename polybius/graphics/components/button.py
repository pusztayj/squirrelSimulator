"""
Author: Trevor Stalnaker
File: button.py

A class that creates and manages a button object
"""

import pygame
from polybius.graphics.utils.textgraphic import TextGraphic
from .multilinetextbox import MultiLineTextBox
from .textbox import TextBox
from polybius.utils.eventwrapper import EventWrapper

class Button(TextGraphic):

    def __init__(self, text, position, font, backgroundColor=(255,255,255),
                 padding=(0,0), fontColor=(0,0,0), borderColor=(0,0,0),
                 borderWidth=0, antialias=True,
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse, dims=None):
        """Initializes the widget with a variety of parameters"""
 
        super().__init__(position, text, font, fontColor, antialias)

        self.setButtonDimensions(font, text, dims, padding)
        
        self._backgroundColor = backgroundColor
        self._borderColor = borderColor
        self._borderWidth = borderWidth

        # Current button colors
        self._currentFontColor = fontColor
        self._currentBackgroundColor = backgroundColor

        # Set the controls for interacting with the button
        self._press = control
        self._release = EventWrapper(self._press.getType()+1,
                                     self._press.getKey, [])
        
        # Set the item that interacts with the button (the mouse by default)
        self._cursor = cursor

        self.updateGraphic()

    def setButtonDimensions(self, font, text, dims, padding):
        # No dimensions provided by designer
        if dims == None:
            t = text.split("\n")
            height = 0
            width = 0
            for line in t:
                w, h = font.size(line)
                height += h
                width = max(width, w)
            self._width = width + (padding[0] * 2)
            self._height = height + (padding[1] * 2)
            self._padding = padding
        # Dimensions specified by designer
        else:
            self._width = dims[0]
            self._height = dims[1]
            self._padding = padding

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

    def handleEvent(self, event, func, args=None, offset=(0,0)):
        """Handles events on the button"""
        if args != None and type(args) not in (tuple, list):
            args = (args,)
        rect = self.getCollideRect()
        rect = rect.move(offset[0],offset[1])
        if self._press.check(event):
            if rect.collidepoint(self._cursor.get_pos()):
                self.buttonPressed()
                if args == None:
                    func()
                else:
                    func(*args)
        elif self._release.check(event):
                self.setToDefaultStyling()
        elif rect.collidepoint(self._cursor.get_pos()):
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
        t = MultiLineTextBox(self._text, (0,0), self._font,
                    self._currentFontColor, antialias=self._antialias)
        t.center(surf)
        t.draw(surf)

##    def __repr__(self):
##        pos = ("(%d,%d)" % (self._position[0], self._position[1]))
##        padding = ("(%d,%d)" % self._padding)
##        fontColor = ("(%d,%d,%d)" % self._fontColor)
##        backgroundColor = ("(%d,%d,%d)" % self._backgroundColor)
##        borderColor = ("(%d,%d,%d)" % self._borderColor)
##        return ("""Button("%s", %s, font, %s,
##                 padding=%s, fontColor=%s, borderColor=%s,
##                 borderWidth=%d, antialias=%r,
##                 control=%s, cursor=%s)""" % (self._text, pos, backgroundColor,
##                                  padding, fontColor, borderColor,
##                                  self._borderWidth, self._antialias,
##                                  repr(self._press), "pygame.mouse"))
