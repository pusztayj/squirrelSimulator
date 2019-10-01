import pygame
from banner import Banner

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

def main():
    pygame.init()
    pygame.display.set_caption("Merchant MiniGame")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Banner((0,0),(255,0,0),(100,100))

    RUNNING = True

    while RUNNING:
        background.draw(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False





    pygame.quit()


if __name__ == "__main__":
    main()
