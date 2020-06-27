"""
@author: Trevor Stalnaker, Justin Pusztay
File: main.py

The main loop for running Squirrel Simulator
"""

import pygame, random, math
from minigame import *
from player import Player
from economy.merchant import Merchant
from animals import *

SCREEN_SIZE = (1200,500)

instruct = ["Welcome to Squirrel Simulator",
             "Hit ESC to pause the game",
             "Use WASD to move",
             "You must eat acorns to survive.\nCollect them and hit space\nto eat them",
             "Click on animals and mercant huts\nto interact with them",
             "Animals can belong to packs.\nHit E to view your pack",
             "You gain XP points overtime.\nHit R to view XP chart",
             "You can only carry so many acorns.\nHit B to bury acorns.\nYou can dig up piles by right\nclicking with selected tool",
             "Right click to use and equip items"]

def giveAcorns(entity, amount):
   """Gives an entity a given number of acorns"""
   entity.setAcorns(entity.getAcorns() + amount)

def giveXP(entity, amount):
   """Gives an entity a given number of XP"""
   entity.setXP(entity.getXP() + amount)

def spawnMerchant(mainGame, position):
   """Spawns a merchant at a given position"""
   mainGame._merchants.append(Merchant(pos=position))

def fastForward(mainGame, amount):
   """Fastforwards the game clock by a given amount"""
   hourLen = mainGame._worldClock.getHourLength()
   time, mode = amount
   if mode == "hours":
      mainGame._worldClock._time += (time*hourLen)
   if mode == "days":
      mainGame._worldClock._time += (time*hourLen*24)

def setHealth(entity, amount):
   """Sets an entity's health to a given amount"""
   amount = max(0,min(amount,entity.getBaseHealth()))
   entity.setHealth(amount)

def spawnAnimal(mainGame, species, position, friendScore):
   """Spawns an animal given a type, position, and friendScore"""
   animal = Creature(species.lower(), pos=position)
   animal.setFriendScore(friendScore)
   p = Pack(animal)
   animal.setPack(p)
   mainGame._packs.append(p)

# Dictionary of cheat codes
cheatCodes = {1:giveAcorns,2:giveXP,3:spawnMerchant,4:fastForward,5:setHealth,
              6:spawnAnimal}

def main():
   """
   Main loop for the program
   """
   # Initialize the module
   pygame.init()
   pygame.font.init()
   pygame.mixer.init()

   # Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   # Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE) #, pygame.FULLSCREEN)

   # Create an instance of the game clock
   gameClock = pygame.time.Clock()

   # Create the cheat box
   cheatBox = Cheats(SCREEN_SIZE)

   # Create the player and their pack
   player = Player(pos=(200,200))
   playerPack = Pack(player)
   player.setPack(playerPack)
   player.scale(1.5)

   # Create the different levels
   level = MainLevel(playerPack, SCREEN_SIZE, cheatBox)
   merchantLevel = None
   combatLevel = None
   endScreen = None

   # Create the loading screen
   loading = LoadingScreen(SCREEN_SIZE, 1)

   # Create the pause menu
   pWidth = SCREEN_SIZE[0] // 4
   pHeight = 2 * (SCREEN_SIZE[1] // 3)
   pauseMenu = PauseMenu((SCREEN_SIZE[0]//2 - pWidth//2, SCREEN_SIZE[1]//2 - pHeight//2),
                     (pWidth, pHeight))
   pauseMenu.close()

   # Create the controls scroll display
   controls = Controls((SCREEN_SIZE[0]//2 - 209, SCREEN_SIZE[1]//2 - 100),200)
   controls.close()

   # Create the title display
   titleScreen = TitleScreen(SCREEN_SIZE)

   # Create the name input interface
   nameInput = NameInput(player, SCREEN_SIZE)

   # Create the tutorial window
   tutorial = Instructions((SCREEN_SIZE[0]//2-150,
                            SCREEN_SIZE[1]//2-100),
                           instruct)
   tutorial.close()

   # Set the mute option to false
   mute = False
   current_volume = 100

   flicker  = False # Used to blit the game background over the controls / tutorials
   lag = True #Used to ever so slightly updated paused game at start

   RUNNING = True

   # Set the initial game code to None
   code = None

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      if endScreen != None:
         
         endScreen.draw(screen)
         
      else:
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

         if tutorial.getDisplay():
            tutorial.draw(screen)

         if nameInput.getDisplay():
            nameInput.draw(screen)

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
            
            if not tutorial.getDisplay() and not nameInput.getDisplay():

               if endScreen != None:
                  # Get the code from the endScreen
                  c = endScreen.handleEvent(event)
                  # End the game
                  if c == 0:
                     RUNNING = False
                  # Restart the game
                  elif c == 1:
                     player = Player(pos=(200,200))
                     playerPack = Pack(player)
                     player.setPack(playerPack)
                     player.scale(1.5)
                     level = MainLevel(playerPack, SCREEN_SIZE, cheatBox)
                     merchantLevel = None
                     combatLevel = None
                     endScreen = None
                     lag = True
                     nameInput = NameInput(player, SCREEN_SIZE)
                     if cheatBox.isDisplayed():
                        cheatBox.toggleDisplay()
                     titleScreen._displayed = True
               else:

                  # Open or close the pause display
                  if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) and \
                     (level._atm == None or not level._atm.getDisplay()) and \
                     not loading.isDisplayed() and\
                     not controls.getDisplay():
                     if not (merchantLevel != None and merchantLevel.isActive()):
                        level.setActive(not level.isActive())
                     if pauseMenu.getDisplay():
                        pauseMenu.close()
                     else:
                        pauseMenu.display()
                        for k in player._movement.keys(): player._movement[k] = False

                  # Handle the main level events
                  if level.isActive() and not loading.isDisplayed() and \
                     not pauseMenu.getDisplay():
                      code = level.handleEvent(event)

                  # Handle merchant level events
                  if merchantLevel != None and merchantLevel.isActive() and \
                     not loading.isDisplayed() and \
                     not pauseMenu.getDisplay():
                      code = merchantLevel.handleEvent(event)

                  # Handle combat level events
                  if combatLevel != None and combatLevel.isActive() and \
                     not loading.isDisplayed() and \
                     not pauseMenu.getDisplay():
                      code = combatLevel.handleEvent(event)

                  # Toggle the cheats display
                  if event.type == pygame.KEYDOWN and event.key == pygame.K_c and \
                     event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_SHIFT:
                        cheatBox.toggleDisplay()

                  # Handle events on the cheat box
                  if cheatBox.isDisplayed() and not loading.isDisplayed():
                     cheatCode = cheatBox.handleEvent(event)
                     if cheatCode != None:
                        if cheatCode[0] in (1,2,5):
                           cheatCodes[cheatCode[0]](player, cheatCode[1])
                        if cheatCode[0] in (3,4):
                           cheatCodes[cheatCode[0]](level, cheatCode[1])
                        if cheatCode[0] in (6,):
                           cheatCodes[cheatCode[0]](level,cheatCode[1],cheatCode[2],cheatCode[3])

                  # Handle events on the pause menu
                  if pauseMenu.getDisplay() and not controls.getDisplay():
                     sel = pauseMenu.handleEvent(event)
                     if sel == 1:
                        if merchantLevel == None or not merchantLevel.isActive():
                           level.setActive(True)
                     if sel == 2:
                        tutorial.display()
                     if sel == 3:
                        controls.display()
                     if sel == 4:
                        RUNNING = False
                     if sel == 5:
                        mute = not mute
                        if mute:
                           pygame.mixer.music.set_volume(0)
                        else:
                           pygame.mixer.music.set_volume(current_volume)

                  # Handle events for the controls menu
                  if controls.getDisplay():
                     controls.handleEvent(event)
                     if not controls.getDisplay():
                        flicker = True
            else:

               # Handle events on the tutorial display
               if tutorial.getDisplay():
                  tutorial.handleEvent(event)
                  if not tutorial.getDisplay():
                     flicker = True

               # Handle events on the inital name input
               if nameInput.getDisplay():
                  nameInput.handleEvent(event)
                  if not nameInput.getDisplay():
                     flicker = True
                     # Update the stats display with the new name
                     level._stats.update() 
                     tutorial.display()
                                  
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
         combatLevel = CombatLevel(player, SCREEN_SIZE, code[1], code[2], screen)
         code = None

         # Reset the movement dictionary for the player
         for k in player._movement.keys():
            player._movement[k] = False

         # Display the loading screen
         loading.setDisplay(True)

      # Update the title screen
      if titleScreen.isDisplayed():
         titleScreen.update(ticks)
      # Create the end screen
      elif player.isDead() and endScreen == None:
         pygame.mixer.music.fadeout(500)
         endScreen = EndScreen(SCREEN_SIZE, player)
      # Update the end screen
      elif endScreen != None:
         endScreen.update()
      # Load the level briefly to create a display behind the tutorial
      elif tutorial.getDisplay():
         if lag:
            lag = False
            level.update(ticks)
      # Load the level briefly to create a display behind the nameInput
      elif nameInput.getDisplay():
         if lag:
            lag = False
            level.update(ticks)
      else:
         
         # Update the main level
         if level.isActive() and not loading.isDisplayed():
             level.update(ticks)

         # Update the merchant level
         if merchantLevel != None and merchantLevel.isActive() and \
            not loading.isDisplayed():
             merchantLevel.update(ticks)

         # Update the combat level
         if combatLevel != None and combatLevel.isActive():
            combatLevel.update(ticks)

         # Update the cheat box
         if cheatBox.isDisplayed():
            cheatBox.update(ticks)

         # Update the loading screen
         if loading.isDisplayed():
            loading.update(ticks)
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

