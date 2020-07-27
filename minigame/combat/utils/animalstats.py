import pygame

from polybius.graphics.textbox import TextBox
from graphics.happinessface import HappinessFace
from polybius.graphics.window import Window
from polybius.graphics.button import Button

from minigame.itemblock import ItemBlock
from minigame.threexthreeinventory import threeXthreeInventory

from economy.acorn import Acorn


class AnimalStats(Window):

    def __init__(self,animal,position):
        """
        Creates an animal display for the user to see. It shows relevant
        stats as well as other useful stats for combat. This is created
        when the animal sprite is right clicked on.

        It displays the animal's name, health, acorns, inventory,
        happiness face, and an exit button to close the screen.
        """
        # self._y is used throughout to get good height spacing
        Window.__init__(self)
        self._animal = animal
        self._position = position
        self._xpos = self._position[0]
        self._ypos = self._position[1]
        self._font = pygame.font.SysFont("Times New Roman", 18)
        
        # Text Stat display along with appropriate images
        self._name = TextBox("Name: " + self._animal.getName(),self._position,
                             self._font,(255,255,255))
        text_y = self._name.getHeight()
        # the happiness face text
        self._opinionText = TextBox("Opinion: ",(self._xpos,self._ypos+text_y+\
                                                 8),
                                    self._font,(255,255,255))
        x = self._opinionText.getWidth()
        # checks to see if class is player so no happiness face is drawn
        if str(type(self._animal)) == "<class 'player.Player'>":
            self._opinionText.setText("Opinion: --")
            text_y += self._opinionText.getHeight() + 11
        # creates the happiness face
        else:
            self._opinion = HappinessFace((self._xpos + x,self._ypos+text_y+2))
            self._opinion.setFace(self._animal.getFriendScore())
            text_y += self._opinion.getHeight()

        # the health text
        self._healthtext = TextBox("Health: "+str(self._animal.getHealth())+\
                                   "/100",
                                   (self._xpos,self._ypos+text_y+2),self._font,
                                   (255,255,255))
        text_y += self._healthtext.getHeight()
        # the acorns text
        self._acornsText = TextBox("Acorns: "+str(self._animal.getAcorns()),
                                   (self._xpos,self._ypos+text_y+6),self._font,
                                   (255,255,255))
        x = self._acornsText.getWidth()
        self._acornImg = Acorn((self._xpos+x,self._ypos+text_y+2))

        # Exit Button
        self._exitButton = Button("X",(self._xpos + 400,self._ypos),
                                  self._font,(0,0,0),(100,100,100),25,25,
                           (0,0,0), 1)

        # Inventory Items
        text_y += self._acornsText.getHeight() + 10
        x = self._healthtext.getWidth()
        # weapon text 
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen = self._weaponText.getWidth()
        # draws item block that will have the weapon
        self._weapon = ItemBlock((self._xpos+xlen+5,self._ypos+text_y+10),(50,50), item=self._animal.getEquipItem())
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        # armor text
        self._armorText = TextBox("Armor equipped: ",(self._xpos+xlen+75,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen += self._armorText.getWidth()
        # draws item block that will have the armor
        self._armor = ItemBlock((self._xpos+xlen+80,self._ypos+text_y+10),(50,50), item=self._animal.getArmor())
        # Sets up inventory display screen
        self._inventory = threeXthreeInventory((self._xpos+x+30,self._ypos),(xlen-14,text_y), self._animal)

    def draw(self,screen):
        """
        Draws the interface onto the combat screen
        """
        if self._display == True:
            self._name.draw(screen)
            if str(type(self._animal)) == "<class 'player.Player'>":
                self._opinionText.draw(screen)
            else:
                self._opinionText.draw(screen)
                self._opinion.draw(screen)
            self._exitButton.draw(screen)
            self._healthtext.draw(screen)
            self._acornsText.draw(screen)
            self._acornImg.draw(screen)
            self._inventory.draw(screen)
            self._weaponText.draw(screen)
            self._weapon.draw(screen)
            self._armorText.draw(screen)
            self._armor.draw(screen)

    def handleEvent(self,event):
        """
        Handles how the user interacts with the window.
        """
        self._exitButton.handleEvent(event, self.close)

    def update(self):
        """
        Updates the text based on any changes in animal health or acorns.
        """
        self._healthtext.setText("Health: "+str(self._animal.getHealth())+\
                                   "/100")
        self._acornsText.setText("Acorns: "+str(self._animal.getAcorns()))

