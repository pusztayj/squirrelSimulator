
import pygame, random, math
from minigame.mainlevel import MainLevel
from player import Player
from minigame.merchantlevel import MerchantLevel

SCREEN_SIZE = (1200,500)

def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()
   pygame.font.init()
   pygame.mixer.init()

   #Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   player = Player()
   player.scale(1.5)
   level = MainLevel(player, SCREEN_SIZE)
   merchantLevel = None

   RUNNING = True

   code = None

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      if level.isActive():
          level.draw(screen)

      if merchantLevel != None and merchantLevel.isActive():
          merchantLevel.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

         if event.type == pygame.KEYDOWN and event.key == pygame.K_p and \
            (level._atm == None or not level._atm.getDisplay()):
            level.setActive(not level.isActive())

         if level.isActive():
             code = level.handleEvent(event)

         if merchantLevel != None and merchantLevel.isActive():
             code = merchantLevel.handleEvent(event)

      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      # Set Game Mode to Merchant
      if code != None and code[0] == 1:
          level.setActive(False)
          pygame.mixer.music.fadeout(1000)
          merch = code[1]
          merchantLevel = MerchantLevel(player, merch, SCREEN_SIZE)
          code = None

           # Reset the movement dictionary for the player
          for k in player._movement.keys():
             player._movement[k] = False
             
      elif code != None and code[0] == 0:
          pygame.mixer.music.fadeout(1000)
          level.setActive(True)
          code = None
        
      if level.isActive():
          level.update(ticks)

      if merchantLevel != None and merchantLevel.isActive():
          merchantLevel.update(ticks)
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

