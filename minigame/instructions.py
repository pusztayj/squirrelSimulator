"""
Author: Trevor Stalnaker
File: instructions.py

This class models the how to play instruction manual
"""

from polybius.graphics import *
import pygame

class Instructions(Drawable, Window):

    def __init__(self, position, textLyst):
        """Initializes the instructions interface"""

        Drawable.__init__(self, "", position, worldBound=False)
        Window.__init__(self)

        self._textLyst = textLyst
        self._current = 0

        # Style Attributes
        self._height = 200
        self._width = 300
        self._textFont = pygame.font.SysFont("Times New Roman",20)
        self._font = pygame.font.SysFont("Times New Roman", 16)
        self._fontColor = (255,255,255)
        self._backgroundColor = (0,0,0)
        self._borderColor = (255,255,255)
        self._borderWidth = 1

        self._offset = self.getPosition()

        # Create the buttons

        self._previous = Button("<<<", (25,self._height - (20+15)),
                                self._font,
                                fontColor=self._fontColor,
                                backgroundColor=(80,80,80),
                                dims=(40,20),
                                borderColor=(120,120,120),
                                borderWidth=1)
        self._next = Button(">>>", (self._width - (40 + 25),
                                    self._height - (20+15)),
                            self._font,
                            fontColor=self._fontColor,
                            backgroundColor=(80,80,80),
                            dims=(40,20),
                            borderColor=(120,120,120),
                            borderWidth=1)

        self._exitButton = Button("X", (self._width-21,2),self._font,
                                  backgroundColor=(100,100,100),
                                  dims=(15,15),
                                  borderColor=(255,255,255),
                                  borderWidth=1)

        # Create the page count display

        self._pageCount = TextBox("Page 1/" + str(len(self._textLyst)),
                                  (0,0),self._font,self._fontColor)
        self._pageCount.setPosition((self._width//2 - self._pageCount.getWidth()//2,
                                     self._height - (35)))

        self.updateInstructions()

    def nextSlide(self):
        """Moves the current pointer to the next slide"""
        self._current += 1

    def previousSlide(self):
        """Moves the current pointer to the previous slide"""
        self._current -= 1

    def getCurrent(self):
        """Returns the pointer to the current slide"""
        return self._current

    def closeAndReset(self):
        """Closes the window and resets the pointer"""
        self._current = 0
        self.close()

    def handleEvent(self, event):
        """Handles events on the instructions interface"""
        if self._current > 0:
            self._previous.handleEvent(event, self.previousSlide,offset=self._offset)
        if self._current < len(self._textLyst)-1:
            self._next.handleEvent(event, self.nextSlide,offset=self._offset)
        self._exitButton.handleEvent(event, self.closeAndReset,offset=self._offset)
        self.updateInstructions()

    def updateInstructions(self):
        """Updates the instructions display as the slides change"""

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        if self._current > 0:
            self._previous.draw(surf)
        if self._current < len(self._textLyst)-1:
            self._next.draw(surf)
        self._exitButton.draw(surf)

        self._text = MultiLineTextBox(self._textLyst[self._current], (0,0), self._textFont,
                                          self._fontColor, self._backgroundColor)
        self._text.setPosition((self._width//2 - self._text.getWidth()//2,
                                self._height//3 - self._text.getHeight()//2))
        self._text.draw(surf)
        self._pageCount.setText("Page " + str(self._current+1) + "/" + \
                                str(len(self._textLyst)))
        self._pageCount.draw(surf)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
