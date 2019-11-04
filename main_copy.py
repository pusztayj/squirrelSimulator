
import pygame, random, math
from mainlevel import MainLevel
from player import Player

SCREEN_SIZE = (1200,500)

def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()
   pygame.font.init()

   #Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   player = Player()
   level = MainLevel(player, SCREEN_SIZE)

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      if level.isActive():
          level.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

         if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            level.setActive(not level.isActive())

         if level.isActive():
             level.handleEvent(event)

      #Calculate ticks
      ticks = gameClock.get_time() / 1000
        
      if level.isActive():
          level.update(ticks)
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

