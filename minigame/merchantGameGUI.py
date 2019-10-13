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


SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)
FLAG = False
a = None

def buyButtonFunc(b,merchant):
    global FLAG; FLAG = True
    item = merchant.getInventory()[0]
    global a; a = getInfoCard(b,(500,300))
    

def sellButtonFunc():
    print("Sell Item")

def main():
    #print(u"\xA3"+"200")
    pygame.init()
    pygame.display.set_caption("Merchant MiniGame")

    font = pygame.font.SysFont("Times New Roman", 16)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Banner((0,0),(255,0,0),(500,1200))
    merchant = Turtle(pos=(800,150))
    merchantMind = Merchant()
    merchant.flip()
    merchant.scale(1.5)

    inventory_name = [x.getName() for x in merchantMind.getInventory()]
    inventory_text = str()
    for x in merchantMind.getInventory():
        inventory_text += str(x.getName()) + "\n"
    merchant_items = makeMultiLineTextBox(inventory_text,(0,0), font, (255,255,255),(0,0,0))

    scrollBox = ScrollBox((100,100),(250,300), merchant_items)

    buyButton = Button("Buy", (100,47), font, (0,0,0), (40,225,255), 50, 75,(255,255,255),2)
    sellButton = Button("Sell", (175,47), font, (0,0,0), (40,80,255), 50, 75,(255,255,255),2)
    
    tradeDesk = TradeDesk()

    RUNNING = True

    b = Squirrel()
    
    

    while RUNNING:
        background.draw(screen)
        merchant.draw(screen)
        tradeDesk.draw(screen)
        scrollBox.draw(screen)
        buyButton.draw(screen)
        sellButton.draw(screen)
        if FLAG == True:
            a.draw(screen)            
        
        pygame.display.flip()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
            buyButton.handleEvent(event, buyButtonFunc,b,merchantMind)
            sellButton.handleEvent(event, sellButtonFunc)
            scrollBox.move(event)





    pygame.quit()


if __name__ == "__main__":
    main()
