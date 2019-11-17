
import pygame
from graphics import TextBox

class LoadingScreen():

    def __init__(self, screensize, time):

        self._font = pygame.font.SysFont("Times New Roman", 28)
        self._text = TextBox("Loading", (0,0), self._font, (255,255,255))
        pos = ((screensize[0]//2) - (self._text.getWidth()//2),
               (screensize[1]//2) - (self._text.getHeight()//2))
        self._text.setPosition(pos)

        self._background = pygame.Surface(screensize)
        self._background.fill((0,0,0))
        
        self._state = 0
        self._textStates = ["Loading","Loading.","Loading..","Loading..."]
        self._dotTime = .25
        self._timer = self._dotTime

        self._displayed = False

        self._displayTime = time
        self._displayTimer = self._displayTime

    def isDisplayed(self):
        return self._displayed

    def setDisplay(self, display):
        self._displayed = display
        if self._displayed == True:
            self._displayTimer = self._displayTime

    def draw(self, screen):
        screen.blit(self._background, (0,0))
        self._text.draw(screen)

    def update(self, ticks):
        if self._displayTimer < 0:
            self.setDisplay(False)
        else:
            if self._timer < 0:
                self._timer = self._dotTime
                self._state += 1
                self._text.setText(self._textStates[self._state%4])
            else:
                self._timer -= ticks
            self._displayTimer -= ticks
        
