"""
Author: Trevor Stalnaker
File: steal.py

The user interface for stealing from NPCs
"""

import pygame, random
from polybius.graphics import *

class Steal(Window):

    def __init__(self, player, entity, SCREEN_SIZE):
        """Initializes the theft interface"""
        
        Window.__init__(self)

        self._baseChance = 40
        self._baseTrustHit = 8

        self._player = player
        self._entity = entity

        # Style Attributes
        self._position = (SCREEN_SIZE[0]//2 - 225//2,100)
        self._font = pygame.font.SysFont("Times New Roman", 22)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._width = 225
        self._height = 100
        self._borderWidth = 2
        self._borderColor = (0,0,0)
        self._backgroundColor = (139,79,59)

        stealPos = (self._position[0] + 30, self._position[1] + 55)
        self._stealButton = Button("Steal", stealPos, self._font, (0,0,0),
                                  (40,80,150), 25, 75, (0,0,0), 2)
        cancelPos = (self._position[0] + 115, self._position[1] + 55)
        self._cancelButton = Button("Cancel", cancelPos, self._font, (0,0,0),
                                  (200,0,0), 25, 75, (0,0,0), 2)
        acornPos = (self._position[0] + 25, self._position[1] + 20)
        self._acorns = TextBox("Acorns: ", acornPos, self._font, (0,0,0))
        acornAvailPos = (self._position[0] + 165, self._position[1] + 20)
        self._acornsAvailable = TextBox("/ " + str(entity.getAcorns()),
                               acornAvailPos, self._font, (0,0,0))
        stealPos = (self._position[0] + 105, self._position[1] + 22)
        self._stealAcorns = TextInput(stealPos, self._font, (50,20),
                                      numerical=True, defaultText="0",
                                      clearOnActive=True,borderWidth=1)

        self._popupWindow = PopupWindow("", (0,0), (285,100), self._font,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((SCREEN_SIZE[0]//2 - self._popupWindow.getWidth()//2,
                                       SCREEN_SIZE[1]//3 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

        self._bustedRobbery = False

    def handleEvent(self, event):
        """Handles events for the theft interface"""
        if self._popupWindow.getDisplay():
            self._popupWindow.handleEvent(event)
        else:
            self._stealButton.handleEvent(event, self.executeTheft)
            self._cancelButton.handleEvent(event, self.close)
            self._stealAcorns.handleEvent(event)
            return self.checkRobbery()
            
    def executeTheft(self):
        """Executes the stealing logic"""
        loot = self._stealAcorns.getInput()
        if loot.isdigit():
            loot = int(loot)
            if loot == 0:
                self._popupWindow.setText("You are not stealing any Acorns")
                self._popupWindow.display()
            elif self._entity.getAcorns() < loot:
                self._popupWindow.setText(self._entity.getName() + " does not have the Acorns")
                self._popupWindow.display()
            elif self._player.getAcorns() + loot > self._player.getCheekCapacity():
                self._popupWindow.setText("You can't hold all those acorns")
                self._popupWindow.display()
            else:
                lootChance = random.randint(1,100)
                odds = (self._baseChance - (loot//2)) + self._player.getStealth()
                if lootChance < odds:
                    self._entity.setAcorns(self._entity.getAcorns() - loot)
                    self._player.setAcorns(self._player.getAcorns() + loot)
                    self._popupWindow.setText(str(loot) + " Acorns stolen")
                    self._popupWindow.display()
                else:
                    self._entity.changeFriendScore(-(self._baseTrustHit + (loot * 0.75))) # 2 Acorns = 1.5 Friend Points
                    self._popupWindow.setText("You failed to steal the acorns\n"+
                                              self._entity.getName() + " will remember this")
                    self._popupWindow.display()
                    if self._entity.getFriendScore() < 15:
                        self._bustedRobbery = True

    def checkRobbery(self):
        """Checks if a robbery was busted"""
        bust = self._bustedRobbery
        self._bustedRobbery = False
        return bust

    def draw(self, screen):
        """Draw the theft interface to the screen"""
        
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
        self._cancelButton.draw(screen)
        self._stealButton.draw(screen)
        self._stealAcorns.draw(screen)
        self._acornsAvailable.draw(screen)
        self._acorns.draw(screen)
        if self._popupWindow.getDisplay():
            self._popupWindow.draw(screen)

    def update(self):
        """Update the number of animals available for theft"""
        self._acornsAvailable.setText("/ " + str(self._entity.getAcorns()))
        
