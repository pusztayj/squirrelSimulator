
from drawable import Drawable
import pygame
from textbox import TextBox
from button import Button
from textinput import TextInput

class ATM(Drawable):

    def __init__(self, player, hole):
        super().__init__("",(50,25),worldBound=False)

        self._player = player
        self._hole = hole

        # Style Attributes
        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._borderColor = (0,0,0)
        self._borderWidth = 5
        self._width = 1100
        self._height = 450
        self._backgroundColor = (255,0,0)

        self._offset = (50,25)
        
        # Buttons
        self._withdrawButton = Button("Withdraw", (120,50), self._font,(0,0,0),
                                      (0,255,0),40,150,(0,0,0), 2)
        self._depositButton = Button("Deposit", (120,100), self._font,(0,0,0),
                                      (255,225,225),40,150,(0,0,0), 2)
        # Text Inputs
        self._holeName = TextInput((200,10), self._font,(200,30),maxLen=12,
                                   defaultText=self._hole.getName(),
                                   borderWidth=0, backgroundColor=(255,0,0),
                                   color=(255,255,255), highlightColor=(0,0,0))
        self._withdrawAmount = TextInput((10,50), self._font,(90,40),maxLen=4,numerical=True)
        self._depositAmount  = TextInput((10,100), self._font,(90,40),maxLen=4,numerical=True)

        # Text Boxes
        self._title = TextBox("Hole Name: ", (10,10), self._font, (255,255,255))
        self._currentBalance = TextBox("Your Current Balance: " + str(self._hole.getAcorns()),
                                       (400,50), self._font, (255,255,255))
        self._carrying = TextBox("On You: " + str(self._player.getAcorns()),
                                 (400,90), self._font, (255,255,255))
        
        self.__updateATM()

    def deposit(self):
        amount = self._depositAmount.getInput()
        if amount != "":
            amount = int(amount)
            if amount <= self._player.getAcorns():
                self._player.setAcorns(self._player.getAcorns() - amount)
                self._hole.setAcorns(self._hole.getAcorns() + amount)

    def withdraw(self):
        amount = self._withdrawAmount.getInput()
        if amount != "":
            amount = int(amount)
            if amount <= self._hole.getAcorns():
                self._player.setAcorns(self._player.getAcorns() + amount)
                self._hole.setAcorns(self._hole.getAcorns() - amount)

    def handleEvent(self, event):
        self._withdrawButton.move(event, self.withdraw, offset=self._offset)
        self._withdrawAmount.handleEvent(event, offset=self._offset)
        self._depositButton.move(event, self.deposit, offset=self._offset)
        self._depositAmount.handleEvent(event, offset=self._offset)
        self._holeName.handleEvent(event, (self._holeName.getInput()), offset=self._offset, func=self._hole.setName)
        self.__updateATM()
        
    def __updateATM(self):

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Add Widgets
        self._title.draw(surf)
        self._holeName.draw(surf)
        self._withdrawButton.draw(surf)
        self._withdrawAmount.draw(surf)
        self._depositButton.draw(surf)
        self._depositAmount.draw(surf)
        self._currentBalance.setText("Current Balance: " + str(self._hole.getAcorns()))
        self._currentBalance.draw(surf)
        self._carrying.setText("Carrying: " + str(self._player.getAcorns()))
        self._carrying.draw(surf)
        
        Button("X", (self._width-45,10),self._font,(0,0,0),(100,100,100),25,25,
               (0,0,0), 1).draw(surf)
        

        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack

    
        
