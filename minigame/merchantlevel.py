import pygame, random
from graphics import *
from animals import *
from economy.tradedesk import TradeDesk
from economy.merchant import Merchant
from economy.transactions import merchantTransaction
from modules import Drawable, Vector2, SoundManager
from player import Player
from items.items import *
from level import Level

class MerchantLevel(Level):

    def __init__(self,player,merchant,SCREEN_SIZE):
        super().__init__()

        self._SCREEN_SIZE = (1200,500)
        self._WORLD_SIZE = (1200,500)

        self._songs = ["shop1.mp3","shop2.mp3","shop3.mp3"]
        self._currentSong = random.choice(self._songs)

        # fonts
        self._font = pygame.font.SysFont("Times New Roman", 16)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        # player
        self._player = player
        self._player_items = [{"text": item.getName(),"func": self.selectMerchantItem,"args":item} \
                      for item in self._player.getInventory()]
        self._playerSelect = ScrollSelector((100,100),(250,300),30,self._player_items,(0,0,0))
        # merchant
        self._merchant = Turtle(pos=(1000,170), worldBound=False)
        self._merchant.flip()
        self._merchant.scale(1.5)
        self._merchantMind = merchant
        self._merchant_items = [{"text": item.getName(),"func": self.selectMerchantItem,"args":item} \
                      for item in self._merchantMind.getInventory()]
        self._merchantSelect = ScrollSelector((100,100),(250,300),30,self._merchant_items,(0,0,0))
        

        # graphics settings
        self._FLAG = True
        self._itemCard = None
        self._popup = None
        self._RUNNING = True

        # background
        self._background = Drawable("merchantForest2.png", Vector2(0,0), worldBound=False)

        # tranasction button
        self._executeTransaction = Button("Execute Transaction",(471,375),
                                         self._font,(255,255,255),(34,139,34),50,145,borderWidth = 2)

        self._cancelTransaction = Button("Cancel Transaction",(627,375),
                                         self._font,(255,255,255),(207,51,17),50,145,borderWidth = 2)
        # trade desk
        self._tradeDesk = TradeDesk()

        # tabs
        self._tabs = Tabs(["Buy","Sell"], (100,47), self._font, (0,0,0), (255,255,255), (200,50),
               (0,0,0),(255,255,255))

        # text boxes for player/merchant money
        self._playerMoney = TextBox("Your money: $" + str(self._player.getAcorns()), (791,375), self._textFont, (255,255,255))
        self._merchantMoney = TextBox(self._merchantMind.getName() + "'s money: $" + str(self._merchantMind.getAcorns()),
                            (795,410), self._textFont, (255,255,255))

        self._exitButton = Button("X", (self._SCREEN_SIZE[0]-45,10),self._font,(0,0,0),
                          (100,100,100),25,25,(0,0,0), 1)

        SoundManager.getInstance().playMusic(self._currentSong)

        
    def selectMerchantItem(self,item):
        self._itemCard = ItemCard(item)

    def updateDisplay(self):
        if self._tabs.getActive() == 0:
            return True
        else:
            return False

    def transaction(self,item):
        if self._itemCard != None:
            if self._tabs.getTabs()[self._tabs.getActive()].getText() == "Buy":  
                if self._player.getAcorns() < item.getValue():
                    text = "You do not have the money!"
                    self._itemCard = None
                elif not self._player.getInventory().hasSpace():
                    text = "You do not have space for this item!"
                    self._itemCard = None
                else:
                    merchantTransaction(self._player,self._merchantMind,item)
                    text = self._merchantMind.getMerchantSpeak()
                    self._itemCard = None
            elif self._tabs.getTabs()[self._tabs.getActive()].getText() \
                 == "Sell":
                 merchantTransaction(self._merchantMind,self._player,item)
                 text = self._merchantMind.getMerchantSpeak()
                 self._itemCard = None
            font = pygame.font.SysFont("Times New Roman", 16)
            self._popup = PopupWindow(text,(471,166),(303,158),
                                font,(255,255,255),(0,0,0),(255,255,255),(30,30),
                                font,(0,0,0),borderWidth = 3)

    def cancelTransaction(self):
        self._itemCard = None

    def draw(self,screen):
        self._background.draw(screen)
        self._merchant.draw(screen)
        self._tradeDesk.draw(screen)
        self._playerMoney.draw(screen)
        self._merchantMoney.draw(screen)
        if self._FLAG:
            self._merchantSelect.draw(screen)
        else:
            self._playerSelect.draw(screen)
        if self._itemCard != None:
            self._itemCard.getCard().draw(screen)
            self._executeTransaction.draw(screen)
            self._cancelTransaction.draw(screen)
        self._tabs.draw(screen)
        if self._popup != None and self._popup.getDisplay():
            self._popup.draw(screen)
        self._exitButton.draw(screen)

    def handleEvent(self,event):
        self._exitButton.handleEvent(event, self.setActive, False)
        if not self.isActive():
            return (0,)
        self._tabs.handleEvent(event)
        if self._popup == None or not self._popup.getDisplay():
            if self._FLAG:
                self._merchantSelect.handleEvent(event)
            else:
                self._playerSelect.handleEvent(event)
        if self._itemCard != None:
            self._itemCard.getCard().move(event)
            if self._popup == None or not self._popup.getDisplay():
                self._executeTransaction.handleEvent(event, self.transaction,self._itemCard.getItem())
                self._cancelTransaction.handleEvent(event, self.cancelTransaction)
            self._playerSelect.updateSelections([{"text": item.getName(),"func": self.selectMerchantItem,"args":item} \
                  for item in self._player.getInventory()])
            self._merchantSelect.updateSelections([{"text": item.getName(),"func": self.selectMerchantItem,"args":item} \
                  for item in self._merchantMind.getInventory()])
        if self._popup != None:
            self._popup.handleEvent(event)

    def update(self,ticks):
        self._FLAG = self.updateDisplay()
        self._playerMoney.setText("Your money: $" + str(self._player.getAcorns()))
        self._merchantMoney.setText(self._merchantMind.getName() + "'s money: $" + str(self._merchantMind.getAcorns()))

        if not pygame.mixer.music.get_busy():
            temp = self._currentSong
            while temp == self._currentSong:
                self._currentSong = random.choice(self._songs)
            SoundManager.getInstance().playMusic(self._currentSong)
