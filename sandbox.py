
import pygame, random
from graphics.banner import Banner
from graphics.textbox import TextBox
from graphics.textinput import TextInput
from graphics.popup import Popup
from graphics.progressbar import ProgressBar
from graphics.statdisplay import StatDisplay
from graphics.scrollselector import ScrollSelector
from graphics.mask import Mask
from modules.vector2D import Vector2
from modules.drawable import Drawable
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from minigame.atm import ATM
from animals.chipmunk import Chipmunk

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()
   pygame.font.init()

   font = pygame.font.SysFont("Times New Roman", 32)

   #Update the title for the window
   pygame.display.set_caption('Sandbox')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   s1 = [{"text":"Button One", "func":print, "args":"One"},
         {"text":"Button Two", "func":print, "args":"Two"}]

   scrollOne = ScrollSelector((10,10), (100,100), 100, s1, (0,0,0))
   #scrollTwo = ScrollSelector((10,10), (100,200), s2, (0,0,0))

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      screen.fill((180,120,80))

      scrollOne.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

         scrollOne.handleEvent(event)
            
                    
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      #Update the player's position
      #player.update(WORLD_SIZE, ticks)
      
      #Update the offset based on the player's location
     #player.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)


   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

