"""
Author: Trevor Stalnaker
File: textinput.py

A class that creates and manages textual input boxes
"""

from polybius.graphics.utils.textgraphic import TextGraphic
from polybius.utils import Timer, EventWrapper, KEY_IDENTIFIER
from polybius.managers import CURSOR
from .textbox import TextBox
import pygame, string

class TextInput(TextGraphic):

    def __init__(self, position, font, dimensions, color=(0,0,0),
                 borderWidth=2, backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderHighlight=(100,100,200),
                 backgroundHighlight=(225,225,255), maxLen=10,
                 numerical=False, highlightColor=(0,0,0), defaultText="",
                 clearOnActive=False, allowNegative=False, antialias=True,
                 allowSymbols=True, updateCursor=True):
        """Initializes the widget with a variety of parameters"""
        super().__init__(position, "", font, color, antialias)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._defaultBorderWidth = borderWidth
        self._defaultBorderColor = borderColor
        self._borderHighlight = borderHighlight
        self._defaultBackgroundColor = backgroundColor
        self._backgroundHighlight = backgroundHighlight
        self._backgroundColor = backgroundColor
        self._textbox = TextBox(defaultText,(0,0),font,color,antialias)
        self._maxLen = maxLen
        self._active = False
        self._clearOnActive = clearOnActive
        self._numerical = numerical
        self._allowNegative = allowNegative
        self._borderColor = self._defaultBorderColor
        self._borderWidth = borderWidth
        self._highlightColor = highlightColor
        self._allowSymbols = allowSymbols
        
        self._pointer = 0
        self._cursorTimer = Timer(.5)
        self._displayCursor = False

        self._deleteDelayTimer = Timer(.5)
        self._deleteTimer = Timer(.2)
        self._deleting = False
        self._realDeletes = False

        self._updateCursor = updateCursor
        self._ibeam = False

        self.updateGraphic()

    def isActive(self):
        return self._active

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
        self._textbox.setFontColor(self._fontColor)
        self.updateGraphic()

    def _makeActive(self, text):
        self._active = True
        self._pointer = len(text)
        self.displayActive()

    def _makeInActive(self):
        self._active = False
        self.displayPassive()
        
    def handleEvent(self, event, *args, offset=(0,0), func=None,
                    clearOnEnter=False):
        """Handle events on the text input"""
        text = self._textbox.getText()
        rect = self.getCollideRect()
        rect = rect.move(offset[0], offset[1])

        if rect.collidepoint(CURSOR.getPosition()):
            if not self._ibeam:
                CURSOR.setCursor("ibeam")
                self._ibeam = True
        else:
            if self._ibeam:
                CURSOR.setToDefault()
                self._ibeam = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if rect.collidepoint(event.pos):
                self._makeActive(text)
            else:
                self._makeInActive()
                         
        elif event.type == pygame.KEYDOWN and self._active:

            # Check if backspace was pressed
            # TO-DO Handle keydown
            if event.key == pygame.K_BACKSPACE:
                self.deleteAtPointer()
                self._deleting = True
                
            

            self.movePointer(event, text)
                            
            if len(text) < self._maxLen:
                self.addCharacter(text, event)
                    
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.onPressEnter(func, args, clearOnEnter)
                
            self.updateGraphic()

        elif event.type == pygame.KEYUP and self._active:
            if event.key == pygame.K_BACKSPACE:
                self._deleting = False
                self._realDeletes = False
                self._deleteTimer.resetTimer()

    def handleDeleting(self):
        if self._deleting:
            self.deleteAtPointer()
            self.updateGraphic()

    def deleteAtPointer(self):
        text = self._textbox.getText()
        newText = text[:self._pointer-1] + text[self._pointer:]
        self._textbox.setText(newText)
        self._pointer = max(0,self._pointer - 1)

    def movePointer(self, event, text):
        if event.key == pygame.K_RIGHT:
            self._pointer = min(len(text), self._pointer+1)
        if event.key == pygame.K_LEFT:
            self._pointer = max(0, self._pointer-1)

    def onPressEnter(self, func, args, clearOnEnter):
        self._active = False
        self.displayPassive()
        if func != None:
            func(*args)
        if clearOnEnter:
            self._textbox.setText("")
            self._pointer = 0

    def addCharacter(self, text, event):
        newChar = KEY_IDENTIFIER.getChar(event)
        if self._numerical:
            if not newChar.isnumeric():
                if (not newChar == "-") or not self._allowNegative:
                    newChar = ""
        elif not self._allowSymbols:
            if newChar in string.punctuation:
                newChar = ""                   
        if newChar != "":
            newText = text[:self._pointer] + newChar + text[self._pointer:]
            self._textbox.setText(newText)
            self._pointer += 1
        
    def getInput(self):
        """Get the current input text"""
        return self._textbox.getText()

    def setText(self, text):
        """Set the text displayed in the input bar"""
        self._textbox.setText(text)
        self._pointer = len(text)
        self.updateGraphic()

    def getBorderColor(self):
        return self._defaultBorderColor

    def getBorderWidth(self):
        return self._defaultBorderWidth

    def getBackgroundColor(self):
        return self._defaultBackgroundColor

    def setFontColor(self, color):
        self._fontColor = color
        self._textbox.setFontColor(color)
        self.updateGraphic()

    def setFont(self, font):
        self._font = font
        self._textbox.setFont(font)
        self.updateGraphic()

    def setBackgroundColor(self, color):
        self._defaultBackgroundColor = color
        self._backgroundColor = color
        self.updateGraphic()

    def setBorderColor(self, color):
        self._defaultBorderColor = color
        self._borderColor = color
        self.updateGraphic()

    def setBorderWidth(self, width):
        self._defaultBorderWidth = width
        self._borderWidth = width
        self.updateGraphic()

    def setBorderHighlight(self, color):
        self._borderHighlight = color

    def setBackgroundHighlight(self, color):
        self._backgroundHighlight = color

    def setDimensions(self, dims):
        self._width = dims[0]
        self._height = dims[1]
        self.updateGraphic()

    def update(self, ticks):
        self._cursorTimer.update(ticks, self.toggleCursor)
        if self._deleting and not self._realDeletes:
            self._deleteDelayTimer.update(ticks, self.realDeletes)
        if self._deleting and self._realDeletes:
            self._deleteTimer.update(ticks, self.handleDeleting)

    def realDeletes(self):
        self._realDeletes = True

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
        self._textbox.center(surf, (1/2,1/2))
        self._textbox.draw(surf)
        if self._displayCursor and self._active:
            top, bottom = self.calculateCursorPosition()
            pygame.draw.line(surf, (0,0,0), top, bottom)


        
