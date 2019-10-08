
import pygame
from modules.drawable import Drawable
from graphics.textbox import TextBox
from graphics.button import Button
from graphics.textinput import TextInput
from graphics.window import Window

class ATM(Drawable, Window):

    def __init__(self, player, hole):
        Drawable.__init__(self, "",(50,25),worldBound=False)
        Window.__init__(self)
        
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
        self._exitButton = Button("X", (self._width-45,10),self._font,(0,0,0),(100,100,100),25,25,
               (0,0,0), 1)
        # Text Inputs
        self._holeName = TextInput((200,10), self._font,(200,30),maxLen=12,
                                   defaultText=self._hole.getName(),
                                   borderWidth=0, backgroundColor=(255,0,0),
                                   color=(255,255,255), highlightColor=(0,0,0))
        self._withdrawAmount = TextInput((10,50), self._font,(90,40),maxLen=4,
                                         numerical=True, clearOnActive=True)
        self._depositAmount  = TextInput((10,100), self._font,(90,40),maxLen=4,
                                         numerical=True, clearOnActive=True)

        # Text Boxes
        self._title = TextBox("Hole Name: ", (10,10), self._font, (255,255,255))
        self._currentBalance = TextBox("Your Current Balance: " + str(self._hole.getAcorns()),
                                       (400,50), self._font, (255,255,255))
        self._carrying = TextBox("On You: " + str(self._player.getAcorns()),
                                 (400,90), self._font, (255,255,255))
        
        self.__updateATM()

    def deposit(self, amount):
        if amount != "":
            amount = int(amount)
            if amount <= self._player.getAcorns():
                self._player.setAcorns(self._player.getAcorns() - amount)
                self._hole.setAcorns(self._hole.getAcorns() + amount)

    def withdraw(self, amount):
        if amount != "":
            amount = int(amount)
            if amount <= self._hole.getAcorns():
                self._player.setAcorns(self._player.getAcorns() + amount)
                self._hole.setAcorns(self._hole.getAcorns() - amount)

    def handleEvent(self, event):
        self._withdrawButton.handleEvent(event, self.withdraw, (self._withdrawAmount.getInput()), offset=self._offset)
        self._withdrawAmount.handleEvent(event, (self._withdrawAmount.getInput()), offset=self._offset,
                                         func=self.withdraw, clearOnEnter=True)
        self._depositButton.handleEvent(event, self.deposit, (self._depositAmount.getInput()), offset=self._offset)
        self._depositAmount.handleEvent(event, (self._depositAmount.getInput()), offset=self._offset,
                                        func=self.deposit, clearOnEnter=True)
        self._holeName.handleEvent(event, (self._holeName.getInput()), offset=self._offset,
                                   func=self._hole.setName)
        self._exitButton.handleEvent(event, self.close, offset=self._offset)
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
        self._exitButton.draw(surf)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack

    
        
