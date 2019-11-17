
import pygame
from graphics.textinput import TextInput


class Cheats():

    def __init__(self, screenDimensions):
        self._font = pygame.font.SysFont("Times New Roman", 16)
        textDimensions = (200,30)
        self._input = TextInput((0,screenDimensions[1]-textDimensions[1]),
                                self._font, textDimensions, maxLen=30)
        self._code = None
        self._display = False
        self._delay = .1

    def handleEvent(self, event):
        if self._delay < 0:
            self._input.handleEvent(event, self._input.getInput(), func=self.getCheatCode,
                                clearOnEnter=True)
        if self._code != None:
            c = self._code
            self._code = None
            return c

    def toggleDisplay(self):
        self._display = not self._display
        if self._display:
            self._input._active = True
            self._input.displayActive()
            self._delay = .1
        else:
            self._input._active = False

    def isDisplayed(self):
        return self._display

    def getCheatCode(self, cheat):
        terms = cheat.split()
        if len(terms) == 2:
            if terms[0] == "giveAcorns":
                if terms[1].isdigit():
                    self._code = (1,int(terms[1]))

    def draw(self, screen):
        self._input.draw(screen)

    def update(self, ticks):
        if self._delay >= 0:
            self._delay -= ticks
