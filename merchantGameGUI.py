import pygame
from banner import Banner
from turtle import Turtle
from beaver import Beaver
from squirrel import Squirrel
from tradedesk import TradeDesk
from merchant import Merchant

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

def main():
    pygame.init()
    pygame.display.set_caption("Merchant MiniGame")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Banner((0,0),(255,0,0),(500,1200))
    merchant = Turtle(pos=(800,150))
    merchantMind = Merchant()
    merchant.flip()
    merchant.scale(1.5)
    tradeDesk = TradeDesk()

    RUNNING = True

    while RUNNING:
        background.draw(screen)
        merchant.draw(screen)
        tradeDesk.draw(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False





    pygame.quit()


if __name__ == "__main__":
    main()
