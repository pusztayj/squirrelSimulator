from .retreatfunctions import retreatLostAcorns,retreatItemLost
import pygame
from graphics.textbox import TextBox
from minigame.threexthreeinventory import threeXthreeInventory

class RetreatScreen(object):

    def __init__(self,player):
        """
        In this class we create the retreat screen that the player sees when
        they click the retreat button

        The screen consists of:

        The numbers of acorns the player lost

        Displays the inventory along with items lost
        """
        self._player = player
        # calculates the number of acorns lost
        self._moneyLost = retreatLostAcorns(self._player)
        player.setAcorns(self._player.getAcorns()-self._moneyLost)

        self._font = pygame.font.SysFont("Times New Roman", 20)
        # calculates the number of items lost
        self._itemLost = retreatItemLost(self._player)
        if self._itemLost != None:
            self._player.getInventory().removeItem(self._itemLost)

        # the text that is displayed in the screen
        self._lostMoneyText = TextBox("You lost "+ str(self._moneyLost) + " acorns.",
                                      (0,0),self._font,(255,255,255))
        x = self._lostMoneyText.getWidth()
        self._lostMoneyText.setPosition((600-(x//2),150))
        y = self._lostMoneyText.getHeight()
        if self._itemLost != None:
            self._itemLostText = TextBox("You lost your " + self._itemLost.getName(),
                                         (0,0),self._font,(255,255,255))
            x = self._itemLostText.getWidth()
            self._itemLostText.setPosition((600-(x//2),150+y+5))
            y += self._itemLostText.getHeight()
        self._inventoryText = TextBox("Your inventory: ",(450,150+y+20),
                                     self._font,(255,255,255))

        self._acornsText = TextBox("Acorns: "+str(self._player.getAcorns()),
                                   (0,0),self._font,
                                   (255,255,255))
##        self._acornImg = Acorn((0,0))
        self._acornsText.setPosition((750-(self._acornsText.getWidth()+5),150+y+20))
        #self._acornImg.setPosition((750-self._acornImg.getWidth(),150+y+15))
        y += self._acornsText.getHeight() + 20
        self._inventory = threeXthreeInventory((450,150+y+5),(300,200), self._player)
        
    def draw(self,screen):
        """
        We draw the retreat screen to the screen.
        """
        self._lostMoneyText.draw(screen)
        if self._itemLost != None:
            self._itemLostText.draw(screen)
        self._acornsText.draw(screen)
##        self._acornImg.draw(screen)
        self._inventoryText.draw(screen)    
        self._inventory.draw(screen)
