"""
Author: Trevor Stalnaker
File: nameinput.py

An interface that allows the player to choose their own name
"""

import pygame, random
from graphics import *
from managers.nameManager import NAMES

class NameInput(Window):

    def __init__(self, player, screenSize):
        """Initialize the interface"""

        Window.__init__(self)
        
        self._player = player
        
        # Style Attributes
        self._font = pygame.font.SysFont("Times New Roman", 22)
        self._height = 125
        self._width = 350
        self._borderWidth = 2
        self._borderColor = (0,0,0)
        self._backgroundColor = (139,79,59)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._position = (screenSize[0]//2 - self._width//2,
                          screenSize[1]//2 - self._height//2)

        # Widgets
        self._prompt = TextBox("Please Name Your Squirrel",
                               (0,0), self._font, (0,0,0))
        self._promptPos = (screenSize[0]//2 - self._prompt.getWidth()//2,
                           self._position[1] + 10)
        self._prompt.setPosition(self._promptPos)
        self._inPos = (self._position[0] + 20,
                      self._position[1] + 40)
        self._inputField = TextInput((0,0), self._font, (200,30),
                                      defaultText=player.getName(),
                                      clearOnActive=True,
                                      maxLen=20, borderWidth=1)
        self._inPos = (screenSize[0]//2 - self._inputField.getWidth()//2,
                      self._position[1] + 40)
        self._inputField.setPosition(self._inPos)
        self._randButton = Button("Random", (0,0), self._font, (0,0,0),
                                  (0,120,0), 28, 85, (0,0,0), 2)
        randPos = (self._position[0] +
                   (self._width//3 - self._randButton.getWidth()//2),
                   self._position[1] + 80)
        self._randButton.setPosition(randPos)
        self._contButton = Button("Continue", (0,0), self._font, (0,0,0),
                                  (0,120,0), 28, 85, (0,0,0), 2)
        contPos = (self._position[0] +
                   (2*(self._width//3) - self._contButton.getWidth()//2),
                   self._position[1] + 80)
        self._contButton.setPosition(contPos)

        self._popupWindow = PopupWindow("", (0,0), (285,100), self._font,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((screenSize[0]//2 - self._popupWindow.getWidth()//2,
                                       screenSize[1]//2 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

    def handleEvent(self, event):
        """Handle events for the interfaces widgets"""
        self._randButton.handleEvent(event, self.randomName)
        self._contButton.handleEvent(event, self.confirm)
        self._inputField.handleEvent(event, func=self.nothing)
        self._popupWindow.handleEvent(event)

    def nothing(self):
        """A simple method that does nothing"""
        pass

    def confirm(self):
        """Confirms and updates the player's name"""
        inputText = self._inputField.getInput()
        if inputText != "" and inputText.replace(" ","") != "":
            self._player.rename(inputText)
            self.close()
        else:
            self._popupWindow.setText("Please input a valid name")
            self._popupWindow.display()

    def randomName(self):
        """Gives the player a new random name"""
        name = NAMES.getRandomName()
        self._inputField.setText(name)

    def draw(self, screen):
        """Draw the interface to the screen"""
        
        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        screen.blit(surfBack, self._position)
        
        # Draw widgets
        self._prompt.draw(screen)
        self._inputField.draw(screen)
        self._randButton.draw(screen)
        self._contButton.draw(screen)
        if self._popupWindow.getDisplay():
            self._popupWindow.draw(screen)

