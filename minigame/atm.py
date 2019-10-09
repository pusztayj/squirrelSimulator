
import pygame
from modules.drawable import Drawable
from graphics.textbox import TextBox
from graphics.button import Button
from graphics.textinput import TextInput
from graphics.window import Window
from economy.acorn import Acorn

class ATM(Drawable, Window):

    def __init__(self, player, hole):
        Drawable.__init__(self, "",(50,25),worldBound=False)
        Window.__init__(self)
        
        self._player = player
        self._hole = hole

        # Style Attributes
        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._fontsmall = pygame.font.SysFont("Times New Roman", 16)
        self._borderColor = (0,0,0)
        self._borderWidth = 5
        self._width = 400#1100
        self._height = 250#450
        self._backgroundColor = (139,79,59)

        self._offset = (50,25)

        # Images
        self._acorn1 = Acorn((250,55), worldBound=False)
        self._acorn2 = Acorn((250,105), worldBound=False)
        
        # Buttons
        self._withdrawButton = Button("Withdraw", (10,50), self._font,(0,0,0),
                                      (0,255,0),35,125,(0,0,0), 2)
        self._depositButton = Button("Deposit", (10,100), self._font,(0,0,0),
                                      (233,97,80),35,125,(0,0,0), 2)
        self._exitButton = Button("X", (self._width-45,10),self._font,(0,0,0),(100,100,100),25,25,
               (0,0,0), 1)
        # Text Inputs
        self._holeName = TextInput((0,10), self._font,(200,30),maxLen=15,
                                   defaultText=self._hole.getName(),
                                   borderWidth=0, backgroundColor=self._backgroundColor,
                                   color=(255,255,255), highlightColor=(0,0,0))
        self._withdrawAmount = TextInput((150,50), self._font,(90,35),maxLen=4,
                                         numerical=True, clearOnActive=True)
        self._depositAmount  = TextInput((150,100), self._font,(90,35),maxLen=4,
                                         numerical=True, clearOnActive=True)

        # Text Boxes
        self._currentBalance = TextBox("Your Current Balance: " + str(self._hole.getAcorns()),
                                       (25,150), self._font, (255,255,255))
        self._carrying = TextBox("On You: " + str(self._player.getAcorns()),
                                 (25,180), self._font, (255,255,255))
        self._capacity = TextBox("Storage Capacity: " + \
                                 str(round((1-(self._hole.getAcorns()/self._hole.getCapacity()))*100,3)) + "%",
                                 (200,200), self._fontsmall,
                                 (255,255,255))        
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
##        self._title.draw(surf)
        self._holeName.draw(surf)
        self._withdrawButton.draw(surf)
        self._withdrawAmount.draw(surf)
        self._depositButton.draw(surf)
        self._depositAmount.draw(surf)
        self._currentBalance.setText("Current Balance: " + str(self._hole.getAcorns()))
        self._currentBalance.draw(surf)
        self._carrying.setText("Carrying: " + str(self._player.getAcorns()))
        self._carrying.draw(surf)
        self._capacity.setText("Storage Capacity: " + \
                                 str(round((1-(self._hole.getAcorns()/self._hole.getCapacity()))*100,3)) + "%")
        self._capacity.setPosition(((self._width//2)-(self._capacity.getWidth()//2),self._height - 35))
        self._capacity.draw(surf)
        self._acorn1.draw(surf)
        self._acorn2.draw(surf)
        self._exitButton.draw(surf)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack

    
        
