import pygame
from graphics.banner import Banner
from animals.turtle import Turtle
from animals.beaver import Beaver
from animals.squirrel import Squirrel
from economy.tradedesk import TradeDesk
from economy.merchant import Merchant
from economy.transactions import merchantTransaction
from graphics.scrollbox import ScrollBox
from graphics.textbox import TextBox
from graphics.guiUtils import *
from graphics.button import Button
from graphics.tabs import Tabs
from modules.drawable import Drawable
from modules.vector2D import Vector2
from player import Player
from items.items import *
from graphics.scrollselector import ScrollSelector


# Forest Background
# https://opengameart.org/content/forest-background-art

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)
FLAG = True
itemCard = None

class ItemCard(object):

    def __init__(self, item):
        self._item = item
        self._card = getInfoCard(item,(471,166),(155,300))

    def getItem(self):
        return self._item

    def getCard(self):
        return self._card

def selectMerchantItem(item):
    #global itemCard; itemCard = getInfoCard(item,(471,166),(155,300))
    global itemCard; itemCard = ItemCard(item)


def updateDisplay(tabs):
    if tabs.getActive() == 0:
        return True
    else:
        return False

def buyButtonFunc(tabs,merchant,player,item):
    if itemCard != None:
        if tabs.getTabs()[tabs.getActive()].getText() == "Buy":
            merchantTransaction(player,merchant,item)
        elif tabs.getTabs()[tabs.getActive()].getText() == "Sell":
            merchantTransaction(merchant,player,item)
    else:
        pass
    
def sellButtonFunc():
    global FLAG; FLAG = False

def main():
    
    # sets up pygame info
    pygame.init()
    pygame.display.set_caption("Merchant MiniGame")
    font = pygame.font.SysFont("Times New Roman", 16)
    textFont = pygame.font.SysFont("Times New Roman", 28)

    # makes screen and background
    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = background = Drawable("merchantForest2.png", Vector2(0,0))

    # sets up merchant
    merchant = Turtle(pos=(1000,170))
    merchantMind = Merchant()
    merchant.flip()
    merchant.scale(1.5)
    merchant_items = [{"text": item.getName(),"func": selectMerchantItem,"args":item} \
                      for item in merchantMind.getInventory()]
    merchantSelect = ScrollSelector((100,100),(250,300),30,merchant_items,(0,0,0))

    # sets up player
    player = Player()
    player.getInventory().addItem(Stick())
    player.getInventory().addItem(Berries())
    player.getInventory().addItem(Spear())
    player.getInventory().addItem(LeatherArmor())
    player_items = [{"text": item.getName(),"func": selectMerchantItem,"args":item} \
                      for item in player.getInventory()]
    playerSelect = ScrollSelector((100,100),(250,300),30,player_items,(0,0,0))
    
    # sets up buttons
    executeTrasaction = Button("Execute Transaction",(471,375),font,(255,255,255),(34,139,34),50,156,borderWidth = 2)
    #buyButton = Button("Buy", (100,47), font, (0,0,0), (40,225,255), 50, 75,(255,255,255),2)
    #sellButton = Button("Sell", (175,47), font, (0,0,0), (40,80,255), 50, 75,(255,255,255),2)

    # gets trade desk
    tradeDesk = TradeDesk()

    tabs = Tabs(["Buy","Sell"], (100,47), font, (0,0,0), (255,255,255), (200,50),
               (0,0,0),(255,255,255))

    playerMoney = TextBox("Your money: $" + str(player.getMoney()), (771,375), textFont, (255,255,255))
    merchantMoney = TextBox(merchantMind.getName() + "'s money: $" + str(merchantMind.getMoney()),
                            (775,410), textFont, (255,255,255))

    RUNNING = True

    FLAG = True

    while RUNNING:
        player_items = [{"text": item.getName(),"func": selectMerchantItem,"args":item} \
                      for item in player.getInventory()]
        playerSelect = ScrollSelector((100,100),(250,300),30,player_items,(0,0,0))

        merchant_items = [{"text": item.getName(),"func": selectMerchantItem,"args":item} \
                      for item in merchantMind.getInventory()]
        merchantSelect = ScrollSelector((100,100),(250,300),30,merchant_items,(0,0,0))
        background.draw(screen)
        merchant.draw(screen)
        tradeDesk.draw(screen)
        executeTrasaction.draw(screen)
        playerMoney.draw(screen)
        merchantMoney.draw(screen)
        if FLAG:
            merchantSelect.draw(screen)
        else:
            playerSelect.draw(screen)
        #buyButton.draw(screen)
        #sellButton.draw(screen)
        if itemCard != None:
            itemCard.getCard().draw(screen)

        tabs.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
            #sellButton.handleEvent(event, sellButtonFunc)
            tabs.handleEvent(event)
            
            # handles switching of tabs
            if FLAG:
                merchantSelect.handleEvent(event)    
            else:
                playerSelect.handleEvent(event)
            # updates item draw
            if itemCard != None:
                itemCard.getCard().move(event)
                executeTrasaction.handleEvent(event, buyButtonFunc,tabs,merchantMind,
                                              player,itemCard.getItem())

        FLAG = updateDisplay(tabs)
        playerMoney.setText("Your money: $" + str(player.getMoney()))
        merchantMoney.setText(merchantMind.getName() + "'s money: $" + str(merchantMind.getMoney()))

    pygame.quit()


if __name__ == "__main__":
    main()
