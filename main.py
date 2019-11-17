import pygame, random, math
from minigame.mainlevel import MainLevel
from player import Player
from animals import Pack, Bear, Rabbit
from minigame.merchantlevel import MerchantLevel
from minigame.combatLevel import CombatLevel
from minigame.cheats import Cheats
from minigame.loadingscreen import LoadingScreen

SCREEN_SIZE = (1200,500)

def giveAcorns(entity, amount):
   entity.setAcorns(entity.getAcorns() + amount)

cheatCodes = {1:giveAcorns}

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
   screen = pygame.display.set_mode(SCREEN_SIZE) #, pygame.FULLSCREEN)

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   player = Player(pos=(200,200))
   ally = Bear(pos=(100,100))
   ally2 = Rabbit(pos=(300,300))
   playerPack = Pack(player)
   playerPack.addMember(ally)
   playerPack.addMember(ally2)
   player.scale(1.5)
   level = MainLevel(playerPack, SCREEN_SIZE)
   merchantLevel = None
   combatLevel = None

   cheatBox = Cheats(SCREEN_SIZE)

   loading = LoadingScreen(SCREEN_SIZE, 1)

   RUNNING = True

   code = None

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      if level.isActive():
          level.draw(screen)

      if merchantLevel != None and merchantLevel.isActive():
          merchantLevel.draw(screen)

      if combatLevel != None and combatLevel.isActive():
         combatLevel.draw(screen)

      if cheatBox.isDisplayed():
         cheatBox.draw(screen)

      if loading.isDisplayed():
         loading.draw(screen)

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

         if level.isActive() and not loading.isDisplayed():
             code = level.handleEvent(event)

         if merchantLevel != None and merchantLevel.isActive() and \
            not loading.isDisplayed():
             code = merchantLevel.handleEvent(event)

         if event.type == pygame.KEYDOWN and event.key == pygame.K_c and \
            event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_SHIFT:
               cheatBox.toggleDisplay()

         if cheatBox.isDisplayed() and not loading.isDisplayed():
            cheatCode = cheatBox.handleEvent(event)
            if cheatCode != None:
               cheatCodes[cheatCode[0]](player, cheatCode[1])

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

          # Display the loading screen
          loading.setDisplay(True)
             
      elif code != None and code[0] == 0:
          pygame.mixer.music.fadeout(1000)
          level.setActive(True)
          code = None

          # Display the loading screen
          loading.setDisplay(True)

      # Set Game Mode to Combat
      elif code != None and code[0] == 2:
         level.setActive(False)
         pygame.mixer.music.fadeout(1000)
         combatLevel = CombatLevel(player, SCREEN_SIZE)
         code = None
        
      if level.isActive() and not loading.isDisplayed():
          level.update(ticks)

      if merchantLevel != None and merchantLevel.isActive() and \
         not loading.isDisplayed():
          merchantLevel.update(ticks)

      if combatLevel != None and combatLevel.isActive():
         combatLevel.update(ticks)

      if cheatBox.isDisplayed():
         cheatBox.update(ticks)

      if loading.isDisplayed():
         loading.update(ticks)
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

