"""
@author Justin Pusztay

In this file we create a victory screen that works when the player wins a
combat game.
"""

from .combatUtils import *
from graphics import *

class VictoryScreen(object):

    def __init__(self,dead,player):
        """
        In this class we create the victory screen that the player sees when
        they successfully defeat their enemies.

        The screen consists of:
        A congratulatory statement

        The numbers of acorns looted along with player total number
        of acorns.

        An interface that allows to view the items avaiable for looting
        along with the ability to add the item to their inventory.

        Also gives the ability for player to drop item from their inventory.
        """
        self._dead = dead
        self._player = player

        # acorns looted
        self._lootedAcorns = lootAcorns(self._dead)

        # graphics settings
        self._FLAG = True
        self._itemCard = None
        self._popup = None

        self._addedAcorns = False
        
        # fonts
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        self._font = pygame.font.SysFont("Times New Roman", 16)

        # needed text boxes
        text = "Congratuations! You defeated your enemies."
        self._victoryText = TextBox(text,(100,25),self._textFont,(255,255,255))
        y = self._victoryText.getHeight()
        acorns = min(self._player.getAcorns()+self._lootedAcorns,self._player.getCheekCapacity())
        self._acornLooted = TextBox("Acorns Looted: "+str(self._lootedAcorns),
                                    (100,25+y+2),self._textFont,(255,255,255))
        y += self._acornLooted.getHeight()
        self._acornCount = TextBox("Your Acorns: "+str(acorns),
                                   (100,25+y+2),self._textFont,(255,255,255))
        y += self._acornCount.getHeight()

        # tabs
        self._tabs = Tabs(["Pickup","Drop"], (100,25+y+5), self._font, (0,0,0), (255,255,255), (200,50),
               (0,0,0),(255,255,255))
        y += self._tabs.getHeight()
        
        # items looted
        self._lootedItems = lootItems(self._dead)
        self._lootItems = [{"text": item.getAttribute("name"),"func": self.selectItem,"args":item} \
                      for item in self._lootedItems]
        self._lootedItemSelect = ScrollSelector((100,25+y+10),(250,300),30,self._lootItems,(0,0,0))

        # player items
        self._player_items = [{"text": item.getAttribute("name"),"func": self.selectItem,"args":item} \
                      for item in self._player.getInventory()]
        self._playerSelect = ScrollSelector((100,25+y+10),(250,300),30,self._player_items,(0,0,0))
        self._y = y

        self._executePickUp = Button("Pick up Item",(450,self._y+25-50),
                                         self._font,(255,255,255),(34,139,34),48,140,borderWidth = 2)

        self._executeDrop = Button("Drop Item",(450,self._y+25-50),
                                         self._font,(255,255,255),(34,139,34),48,140,borderWidth = 2)

        self._cancelTransaction = Button("Cancel Transaction",(450+156,self._y+25-50),
                                         self._font,(255,255,255),(207,51,17),48,140,borderWidth = 2)

    def selectItem(self,item):
        """
        This generates the item cards that need to go in the scroll
        box selector
        """
        self._itemCard = ItemCard(item, position = (450,self._y+25+10), scrollBoxSize = (200,300))

    def updateDisplay(self):
        """
        This method is responsible for the which tab is active in the
        display.
        """
        if self._tabs.getActive() == 0:
            return True
        else:
            return False

    def cancelTransaction(self):
        """
        When a transaction is cancled this sets the item card to none
        to longer display it.
        """
        self._itemCard = None

    def pickUpItem(self,item):
        """
        Excecutes the transaction when the player loots an item. 
        """
        if self._player.getInventory().hasSpace():
            self._player.getInventory().addItem(item)
            item.setOwner(self._player)
            self._lootedItems.remove(item)
            self._itemCard = None
            self._popup = None
        else:
            self._itemCard = None
            self._popup = PopupWindow("You have no room in your inventory",
                            (450,self._y+25+10),(270,175),
                        self._font,(255,255,255),(0,0,0),(255,255,255),(30,30),
                        self._font,(0,0,0),borderWidth = 3)

    def dropItem(self,item):
        """
        This drops the item from the players iventory and inserts
        it into the looted items. 
        """
        self._player.getInventory().removeItem(item)
        item.setOwner(None)
        self._lootedItems.append(item)
        self._itemCard = None
        
    def draw(self,screen):
        """
        Draws the victory screen to the screen.
        """
        if not self._addedAcorns:
            self._player.setAcorns(min(self._player.getAcorns()+self._lootedAcorns,self._player.getCheekCapacity()))
            self._addedAcorns = True
        self._victoryText.draw(screen)
        self._acornLooted.draw(screen)
        self._acornCount.draw(screen)
        if self._FLAG: # checks to see if the item can be drawn
            self._lootedItemSelect.draw(screen)
        else:
            self._playerSelect.draw(screen)
        if self._itemCard != None:
            self._itemCard.getCard().draw(screen)
            self._cancelTransaction.draw(screen)
            if self._FLAG:
                self._executePickUp.draw(screen)
            else:
                self._executeDrop.draw(screen)
            
        self._tabs.draw(screen)
        if self._popup != None and self._popup.getDisplay():
            self._popup.draw(screen)

    def handleEvent(self,event):
        """
        Handles all the events for the victory screen.
        """
        self._tabs.handleEvent(event)
        if self._popup == None or not self._popup.getDisplay():
            if self._FLAG:
                self._lootedItemSelect.handleEvent(event)
            else:
                self._playerSelect.handleEvent(event)
        if self._itemCard != None:
            self._itemCard.getCard().move(event)
            if self._popup == None or not self._popup.getDisplay():
                if self._FLAG:
                    self._executePickUp.handleEvent(event,
                                    self.pickUpItem,self._itemCard.getItem())
                else:
                    self._executeDrop.handleEvent(event,
                                    self.dropItem,self._itemCard.getItem())
            self._cancelTransaction.handleEvent(event,
                                        self.cancelTransaction)

            self._playerSelect.updateSelections([{"text": item.getAttribute("name"),"func": self.selectItem,"args":item} \
                      for item in self._player.getInventory()])
            self._lootedItemSelect.updateSelections([{"text": item.getAttribute("name"),"func": self.selectItem,"args":item} \
                      for item in self._lootedItems])
        if self._popup != None:
            self._popup.handleEvent(event)

    def update(self):
        """
        Updates the victory screen.
        """
        if self._FLAG != self.updateDisplay():
            self._itemCard = None
        self._FLAG = self.updateDisplay()

