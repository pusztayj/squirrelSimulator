"""
Author: Trevor Stalnaker, Justin Pusztay
File: main.py

The main loop for running Squirrel Simulator
"""

import pygame, random, math
from minigame import *
from player import Player
from economy.merchant import Merchant
from animals import *

SCREEN_SIZE = (1200,500)

def giveAcorns(entity, amount):
   entity.setAcorns(entity.getAcorns() + amount)

def giveXP(entity, amount):
   entity.setXP(entity.getXP() + amount)

def spawnMerchant(mainGame, position):
   mainGame._merchants.append(Merchant(pos=position))

def fastForward(mainGame, amount):
   hourLen = mainGame._worldClock.getHourLength()
   time, mode = amount
   if mode == "hours":
      mainGame._worldClock._time += (time*hourLen)
   if mode == "days":
      mainGame._worldClock._time += (time*hourLen*24)

def setHealth(entity, amount):
   amount = max(0,min(amount,entity.getBaseHealth()))
   entity.setHealth(amount)

def spawnAnimal(mainGame, species, position, friendScore):
   animal = eval(species.title())(pos=position)
   animal.setFriendScore(friendScore)
   p = Pack(animal)
   animal.setPack(p)
   mainGame._packs.append(p)

cheatCodes = {1:giveAcorns,2:giveXP,3:spawnMerchant,4:fastForward,5:setHealth,
              6:spawnAnimal}

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

   cheatBox = Cheats(SCREEN_SIZE)

   player = Player(pos=(200,200))
   playerPack = Pack(player)
   player.setPack(playerPack)
   player.scale(1.5)
   level = MainLevel(playerPack, SCREEN_SIZE, cheatBox)
   merchantLevel = None
   combatLevel = None

   loading = LoadingScreen(SCREEN_SIZE, 1)

   # Create the pause menu
   pWidth = SCREEN_SIZE[0] // 4
   pHeight = 2 * (SCREEN_SIZE[1] // 3)
   pauseMenu = PauseMenu((SCREEN_SIZE[0]//2 - pWidth//2, SCREEN_SIZE[1]//2 - pHeight//2),
                     (pWidth, pHeight))
   pauseMenu.close()

   controls = Controls((SCREEN_SIZE[0]//2 - 209, SCREEN_SIZE[1]//2 - 100),200)
   controls.close()

   titleScreen = TitleScreen(SCREEN_SIZE)

   flicker  = False

   RUNNING = True

   code = None

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      if level.isActive() or flicker:
          level.draw(screen)
          flicker = False

      if merchantLevel != None and merchantLevel.isActive():
          merchantLevel.draw(screen)

      if combatLevel != None and combatLevel.isActive():
         combatLevel.draw(screen)

      if cheatBox.isDisplayed():
         cheatBox.draw(screen)

      if loading.isDisplayed():
         loading.draw(screen)

      if pauseMenu.getDisplay():
         pauseMenu.draw(screen)

      if controls.getDisplay():
         controls.draw(screen)

      if titleScreen.isDisplayed():
         titleScreen.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT):
            RUNNING = False

         if titleScreen.isDisplayed():
            titleScreen.handleEvent(event)
         else:

            if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) and \
               (level._atm == None or not level._atm.getDisplay()) and \
               not loading.isDisplayed() and\
               not controls.getDisplay():
               level.setActive(not level.isActive())
               if pauseMenu.getDisplay():
                  pauseMenu.close()
               else:
                  pauseMenu.display()
                  for k in player._movement.keys(): player._movement[k] = False

            if level.isActive() and not loading.isDisplayed() and \
               not pauseMenu.getDisplay():
                code = level.handleEvent(event)

            if merchantLevel != None and merchantLevel.isActive() and \
               not loading.isDisplayed() and \
               not pauseMenu.getDisplay():
                code = merchantLevel.handleEvent(event)

            if combatLevel != None and combatLevel.isActive() and \
               not loading.isDisplayed() and \
               not pauseMenu.getDisplay():
                code = combatLevel.handleEvent(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and \
               event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_SHIFT:
                  cheatBox.toggleDisplay()

            if cheatBox.isDisplayed() and not loading.isDisplayed():
               cheatCode = cheatBox.handleEvent(event)
               if cheatCode != None:
                  if cheatCode[0] in (1,2,5):
                     cheatCodes[cheatCode[0]](player, cheatCode[1])
                  if cheatCode[0] in (3,4):
                     cheatCodes[cheatCode[0]](level, cheatCode[1])
                  if cheatCode[0] in (6,):
                     cheatCodes[cheatCode[0]](level,cheatCode[1],cheatCode[2],cheatCode[3])

            if pauseMenu.getDisplay() and not controls.getDisplay():
               sel = pauseMenu.handleEvent(event)
               if sel == 1:
                  if merchantLevel == None or not merchantLevel.isActive():
                     level.setActive(True)
               if sel == 3:
                  controls.display()
               if sel == 4:
                  RUNNING = False

            if controls.getDisplay():
               controls.handleEvent(event)
               if not controls.getDisplay():
                  flicker = True
                  
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

      # Set Game Mode to Main Game
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

         # Reset the movement dictionary for the player
         for k in player._movement.keys():
            player._movement[k] = False

         # Display the loading screen
         loading.setDisplay(True)

      if titleScreen.isDisplayed():
         titleScreen.update(ticks)
      else:
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

