
import pygame, random
from vector2D import Vector2
from drawable import Drawable
from squirrel import Squirrel

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()

   #Store the pygame key codes for simplicity later
   movement_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

   #Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Load the background image
   background = Drawable("background.png", Vector2(0,0))

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   player = Squirrel()

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      background.draw(screen)

      #Draw the player to the screen
      player.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False
            
         elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) \
            and event.key in movement_keys:
            player.move(event)
            
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      #Update the player's position
      player.update(WORLD_SIZE, ticks)
      
      #Update the offset based on the player's location
      player.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)


   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

