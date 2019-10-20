import pygame
from graphics.banner import Banner
from animals.turtle import Turtle
from animals.beaver import Beaver
from animals.squirrel import Squirrel
from economy.tradedesk import TradeDesk
from economy.merchant import Merchant
from graphics.scrollbox import ScrollBox
from graphics.textbox import TextBox
from graphics.guiUtils import *
from graphics.button import Button
from player import Player
from items.items import *
from graphics.scrollselector import ScrollSelector


SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)
FLAG = True
itemCard = None

def selectMerchantItem(item):
    global itemCard; itemCard = getInfoCard(item,(500,300))

def buyButtonFunc():
    global FLAG; FLAG = True
    
def sellButtonFunc():
    global FLAG; FLAG = False

def main():
    
    # sets up pygame info
    pygame.init()
    pygame.display.set_caption("Merchant MiniGame")
    font = pygame.font.SysFont("Times New Roman", 16)

    # makes screen and background
    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Banner((0,0),(255,0,0),(500,1200))

    # sets up merchant
    merchant = Turtle(pos=(800,150))
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
    player_items = [{"text": item.getName(),"func": selectMerchantItem,"args":item} \
                      for item in player.getInventory()]
    playerSelect = ScrollSelector((100,100),(250,300),30,player_items,(0,0,0))
    
    # sets up buttons
    buyButton = Button("Buy", (100,47), font, (0,0,0), (40,225,255), 50, 75,(255,255,255),2)
    sellButton = Button("Sell", (175,47), font, (0,0,0), (40,80,255), 50, 75,(255,255,255),2)

    # gets trade desk
    tradeDesk = TradeDesk()

    RUNNING = True

    while RUNNING:
        background.draw(screen)
        merchant.draw(screen)
        tradeDesk.draw(screen)
        if FLAG:
            merchantSelect.draw(screen)
        else:
            playerSelect.draw(screen)
        buyButton.draw(screen)
        sellButton.draw(screen)
        if itemCard != None:
            itemCard.draw(screen)            
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
            buyButton.handleEvent(event, buyButtonFunc)
            sellButton.handleEvent(event, sellButtonFunc)
            
            # handles switching of tabs
            if FLAG:
                merchantSelect.handleEvent(event)    
            else:
                playerSelect.handleEvent(event)
            # updates item draw
            if itemCard != None:
                itemCard.move(event)

    pygame.quit()


if __name__ == "__main__":
    main()
