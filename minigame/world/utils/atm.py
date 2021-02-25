"""
Author: Trevor Stalnaker
File: atm.py

An interface for interacting with dirt piles
"""

import pygame
from polybius.graphics import Drawable, TextBox, Button, TextInput
from polybius.graphics import Window, PopupWindow


from economy.acorn import Acorn

class ATM(Drawable, Window):

    def __init__(self, player, hole, screensize):
        """Initialize the interface"""
        Drawable.__init__(self, "",(50,25),worldBound=False)
        Window.__init__(self)
        
        self._player = player
        self._hole = hole

        # Style Attributes
        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._fontsmall = pygame.font.SysFont("Times New Roman", 16)
        self._popupFont = pygame.font.SysFont("Times New Roman", 18)
        self._borderColor = (0,0,0)
        self._borderWidth = 5
        self._width = 400
        self._height = 265
        self._backgroundColor = (139,79,59)

        self._offset = (50,25)

        # Images
        self._acorn1 = Acorn((250,55), worldBound=False)
        self._acorn2 = Acorn((250,105), worldBound=False)
        
        # Buttons
        self._withdrawButton = Button("Withdraw", (10,50), self._font,
                                      backgroundColor=(0,255,0),
                                      dims=(125,35),
                                      borderColor=(0,0,0),
                                      borderWidth=2)
        self._depositButton = Button("Deposit", (10,100), self._font,
                                     backgroundColor=(233,97,80),
                                     dims=(125,35),
                                     borderColor=(0,0,0),
                                     borderWidth=2)
        self._exitButton = Button("X", (self._width-45,10),self._font,
                                  backgroundColor=(100,100,100),
                                  dims=(25,25),
                                  borderColor=(0,0,0),
                                  borderWidth=1)
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
        self._maxCapacity = TextBox("Max Capacity: " + str(self._hole.getCapacity()),
                                    (200,250),self._fontsmall,(255,255,255))
        self._maxCapacity.setPosition(((self._width//2)-(self._maxCapacity.getWidth()//2),self._height - 55))
        self.updateATM()


        # Popup Windows
        self._popupWindow = PopupWindow("", (0,0), (285,100), self._popupFont,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((screensize[0]//2 - self._popupWindow.getWidth()//2,
                                       screensize[1]//3 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

    def deposit(self, amount):
        """Executes the deposit logic for a transaction"""
        if amount != "":
            amount = int(amount)
            if amount == 0:
                self._popupWindow.setText("You are not depositing any acorns")
                self._popupWindow.display()
            elif not amount <= self._player.getAcorns():
                self._popupWindow.setText("You do not have that many\nacorns to deposit")
                self._popupWindow.display()
            elif not amount <= self._hole.getCapacity() - self._hole.getAcorns():
                self._popupWindow.setText("This stash can't hold that\n many more acorns")
                self._popupWindow.display()
            else:
                self._player.setAcorns(self._player.getAcorns() - amount)
                self._hole.setAcorns(self._hole.getAcorns() + amount)
        else:
            self._popupWindow.setText("You are not depositing any acorns")
            self._popupWindow.display()

    def withdraw(self, amount):
        """Executes the withdraw logic for a transaction"""
        if amount != "":
            amount = int(amount)
            if amount == 0:
                self._popupWindow.setText("You are not withdrawing any acorns")
                self._popupWindow.display()
            elif not amount <= self._hole.getAcorns():
                self._popupWindow.setText("This stash doesn't have\nthat many acorns")
                self._popupWindow.display()
            elif not amount <= self._player.getCheekCapacity() - self._player.getAcorns():
                self._popupWindow.setText("You can't carry all of\nthose acorns")
                self._popupWindow.display()
            else:
                self._player.setAcorns(self._player.getAcorns() + amount)
                self._hole.setAcorns(self._hole.getAcorns() - amount)
        else:
            self._popupWindow.setText("You are not withdrawing any acorns")
            self._popupWindow.display()

    def handleEvent(self, event):
        """Handles events on the ATM"""
        if self._popupWindow.getDisplay():
            self._popupWindow.handleEvent(event)
        else:
            self._withdrawButton.handleEvent(event, self.withdraw, (self._withdrawAmount.getInput()), offset=self._offset)
            self._withdrawAmount.handleEvent(event, (self._withdrawAmount.getInput()), offset=self._offset,
                                             func=self.withdraw, clearOnEnter=True)
            self._depositButton.handleEvent(event, self.deposit, (self._depositAmount.getInput()), offset=self._offset)
            self._depositAmount.handleEvent(event, (self._depositAmount.getInput()), offset=self._offset,
                                            func=self.deposit, clearOnEnter=True)
            self._holeName.handleEvent(event, (self._holeName.getInput()), offset=self._offset,
                                       func=self._hole.setName)
            if self._hole.getName() != self._holeName.getInput():
                self._hole.setName(self._holeName.getInput())
            self._exitButton.handleEvent(event, self.close, offset=self._offset)
            self.updateATM()

    def draw(self, screen):
        """Draws the ATM to the screen"""
        Drawable.draw(self, screen)
        if self._popupWindow.getDisplay():
            self._popupWindow.draw(screen)
            
    def updateATM(self):
        """Updates the display of the ATM as attributes change"""
        
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
        self._maxCapacity.draw(surf)
        self._acorn1.draw(surf)
        self._acorn2.draw(surf)
        self._exitButton.draw(surf)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack

    
        
