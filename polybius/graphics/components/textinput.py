"""
Author: Trevor Stalnaker
File: textinput.py

A class that creates and manages textual input boxes
"""

from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.utils import Timer
from .textbox import TextBox
import pygame

class TextInput(AbstractGraphic):

    def __init__(self, position, font, dimensions, color=(0,0,0),
                 borderWidth=2, backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderHighlight=(100,100,200),
                 backgroundHighlight=(225,225,255), maxLen=10,
                 numerical=False, highlightColor=(0,0,0), defaultText="",
                 clearOnActive=False, allowNegative=False, antialias=True):
        """Initializes the widget with a variety of parameters"""
        super().__init__(position)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._defaultBorderWidth = borderWidth
        self._defaultBorderColor = borderColor
        self._borderHighlight = borderHighlight
        self._defaultBackgroundColor = backgroundColor
        self._backgroundHighlight = backgroundHighlight
        self._backgroundColor = backgroundColor
        self._font = font
        self._textbox = TextBox(defaultText,(0,0),font,color,antialias)
        self._maxLen = maxLen
        self._active = False
        self._clearOnActive = clearOnActive
        self._numerical = numerical
        self._allowNegative = allowNegative
        self._borderColor = self._defaultBorderColor
        self._borderWidth = borderWidth
        self._color = color
        self._highlightColor = highlightColor
        self._antialias = antialias
        self._allowSymbols = False
        
        self._pointer = 0
        self._cursorTimer = Timer(.5)
        self._displayCursor = False

        self.updateGraphic()

    def displayActive(self):
        """Sets the display mode to active"""
        self._borderColor = self._borderHighlight
        self._borderWidth = self._defaultBorderWidth + 1
        self._backgroundColor = self._backgroundHighlight
        self._textbox.setFontColor(self._highlightColor)
        if self._clearOnActive:
            self._textbox.setText("")
            self._pointer = 0
        self.updateGraphic()

    def displayPassive(self):
        """Sets the display mode to passive"""
        self._borderColor = self._defaultBorderColor
        self._borderWidth = self._defaultBorderWidth
        self._backgroundColor = self._defaultBackgroundColor
        self._textbox.setFontColor(self._color)
        self.updateGraphic()
        
    def handleEvent(self, event, *args, offset=(0,0), func=None,
                    clearOnEnter=False):
        """Handle events on the text input"""
        text = self._textbox.getText()
        rect = self.getCollideRect()
        rect = rect.move(offset[0], offset[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if rect.collidepoint(event.pos):
                self._active = True
                self._pointer = len(text)
                self.displayActive()
            else:
                self._active = False
                self.displayPassive()
                
        elif event.type == pygame.KEYDOWN and self._active:

            # Check if backspace was pressed
            if event.key == 8:
                newText = text[:self._pointer-1] + text[self._pointer:]
                self._textbox.setText(newText)
                self._pointer = max(0,self._pointer - 1)

            # Move the input cursor left and right
            if event.key == pygame.K_RIGHT:
                self._pointer = min(len(text), self._pointer+1)
            if event.key == pygame.K_LEFT:
                self._pointer = max(0, self._pointer-1)
            
            if len(text) < self._maxLen:
                
                newChar = ""
                
                alphaKey = 96 < event.key < 123
                numKey = 47 < event.key < 58
                spaceKey = event.key == 32
                numPadKey = pygame.K_KP0 <= event.key <= pygame.K_KP9
                minusKey = (event.key == pygame.K_KP_MINUS or \
                            event.key ==pygame.K_MINUS)
                symbolKey = 33 < event.key <= 47 or 58 < event.key <= 64
                underscoreKey = event.key == pygame.K_MINUS and \
                                event.mod in [pygame.KMOD_LSHIFT,pygame.KMOD_RSHIFT]
                if alphaKey and not self._numerical:
                    newChar = self.checkForLetters(event)
                elif (spaceKey and not self._numerical) or numKey or \
                     (symbolKey and self._allowSymbols):
                    newChar = chr(event.key)
                elif numPadKey:
                    newChar = chr(event.key-208)
                elif underscoreKey:
                    newChar = "_"
                elif minusKey and (not self._numerical or self._allowNegative):
                    newChar = "-"
                   
                if newChar != "":
                    newText = text[:self._pointer] + newChar + text[self._pointer:]
                    self._textbox.setText(newText)
                    self._pointer += 1
                     
            # Check if the enter key was pressed
            if event.key == 13 or event.key == pygame.K_KP_ENTER:
                self._active = False
                self.displayPassive()
                if func != None:
                    func(*args)
                if clearOnEnter:
                    self._textbox.setText("")
                    self._pointer = 0
            self.updateGraphic()

    def checkForLetters(self, event):
        if event.mod in [pygame.KMOD_CAPS, pygame.KMOD_LSHIFT,
                        pygame.KMOD_RSHIFT]:
            return chr(event.key - 32)
        else:
            return chr(event.key)
        
    def getInput(self):
        """Get the current input text"""
        return self._textbox.getText()

    def setText(self, text):
        """Set the text displayed in the input bar"""
        self._textbox.setText(text)
        self._pointer = len(text)
        self.updateGraphic()

    def update(self, ticks):
        self._cursorTimer.update(ticks, self.toggleCursor)

    def toggleCursor(self):
        self._displayCursor = not self._displayCursor
        self.updateGraphic()

    def getPixelWidth(self, text):
        font = self._font
        width, height = font.size(text)
        return width

    def calculateCursorPosition(self):
        top = self._textbox.getY()
        bottom = top + self._textbox.getHeight() - 4
        text = self._textbox.getText()[:self._pointer]
        x_pos = self._textbox.getX() + self.getPixelWidth(text)
        return ((x_pos, top),(x_pos, bottom))

##    def calculatePointerPlacement(self, eventPos, rect):
##        print("hello")
##        eventx = eventPos[0]
##        basex = rect.x
##        text = self._textbox.getText()
##        tbWidth = self._textbox.getWidth()
##        checkedValues = []
##        minPlacement = 0
##        maxPlacement = len(text)
##        while True:
##            pointer = (minPlacement + maxPlacement) // 2
##            normalx = basex + self.getPixelWidth(text[:pointer])
##            pointerx = (basex + tbWidth)//2 - (normalx // 2)
##            print(pointer)
##            print("Px:", pointerx)
##            print("Ex:",eventx)
##            if eventx < pointerx:
##                maxPlacement = pointer
##            elif eventx > pointerx:
##                minPlacement = pointer
##            else:
##                self._pointer = pointer
##                print("here")
##                break
##            if pointer in checkedValues:
##                self._pointer = pointer
##                break
####                # Find the closest pointer (one to the left and right of optimal)
####                distances = [abs(self.findPointerXCoordinate(p, basex, text)-eventx)
####                  for p in range(pointer-1, pointer+2)]
####                minimum = min(distances)
####                self._pointer = (pointer-1) + distances.index(minimum)
####                "print woah"
####                break
##            checkedValues.append(pointer)

##    def findPointerXCoordinate(self, pointer, basex, text):
##        return basex + self.getPixelWidth(text[:pointer-1])

    def internalUpdate(self, surf):
        """Update the widget's display"""
        y_pos = (self._height // 2) - (self._textbox.getHeight() // 2)
        x_pos = (self._width // 2) - (self._textbox.getWidth() // 2)
        self._textbox.setPosition((x_pos, y_pos))
        self._textbox.draw(surf)
        if self._displayCursor and self._active:
            top, bottom = self.calculateCursorPosition()
            pygame.draw.line(surf, (0,0,0), top, bottom)
        
