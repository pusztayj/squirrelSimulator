"""
@author: Trevor Stalnaker, Justin Pusztay
File: main.py

The main loop for running Squirrel Simulator
"""

import pygame, random, math
from minigame import *
from graphics.ui.menu import Menu
from player import Player

from animals import *
from managers import CONSTANTS, USER_INTERFACE, SOUNDS, CONTROLS

SCREEN_SIZE = CONSTANTS.get("screen_size")

instruct = ["Welcome to Squirrel Simulator",
             "Hit ESC to pause the game",
             "Use WASD to move",    
             "You must eat acorns to survive.\nCollect them and hit space\nto eat them",
             "Click on animals and merchant huts\nto interact with them",
             "Animals can belong to packs.\nHit E to view your pack",
             "You gain XP points over time.\nHit R to view XP chart",
             "You can only carry so many acorns.\nHit B to bury acorns.\nYou can dig up piles by right\nclicking with selected tool",
             "Right click to use and equip items"]

def main():
   """
   Main loop for the program
   """
   # Initialize the module
   pygame.init()
   pygame.font.init()
   pygame.mixer.init()

   #Makes the mouse pointer invisible
   #pygame.mouse.set_visible(False)

   #Makes a custom cursor
   #pygame.mouse.set_cursor()

   # Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   # Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)#, pygame.FULLSCREEN)

   # Create an instance of the game clock
   gameClock = pygame.time.Clock()

   # Create the cheat box
   cheatBox = CheatBox(SCREEN_SIZE)

   # Create the player and their pack
   player = Player(pos=CONSTANTS.get("player_start_pos"))
   playerPack = Pack(player)
   player.setPack(playerPack)
   player.scale(1.5)

   # Create the different levels
   level = MainLevel(playerPack, cheatBox)
   merchantLevel = None
   combatLevel = None
   endScreen = None

   # Create the loading screen
   loading = LoadingScreen(SCREEN_SIZE, 1)

   # Create the pause menu
   pWidth = SCREEN_SIZE[0] // 4
   pHeight = 2 * (SCREEN_SIZE[1] // 3)
   pause_commands = USER_INTERFACE.getControlsForMenu("pause")
   pauseMenu = Menu(((SCREEN_SIZE[0]//2 - pWidth//2), SCREEN_SIZE[1]//2 - pHeight//2),
             (pWidth, pHeight), pause_commands, (37,16), -1)
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
                     player = Player(pos=CONSTANTS.get("player_start_pos"))
                     playerPack = Pack(player)
                     player.setPack(playerPack)
                     player.scale(1.5)
                     level = MainLevel(playerPack, cheatBox)
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
                  if(CONTROLS.get("pause").check(event)) and \
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
                  if CONTROLS.get("display_cheat_box").check(event):
                        cheatBox.toggleDisplay()

                  # Handle events on the cheat box
                  if cheatBox.isDisplayed() and not loading.isDisplayed():
                     cheatCode = cheatBox.handleEvent(event)
                     if cheatCode != None:
                        if cheatCode[0] in cheatBox.getCodesByType(1) and \
                           len(cheatCode)==2:
                           cheatBox.execute((cheatCode[0], player, cheatCode[1]))
                        if cheatCode[0] in cheatBox.getCodesByType(2):
                           cheatBox.execute((cheatCode[0], level, cheatCode[1]))
                        if cheatCode[0] in cheatBox.getCodesByType(3):
                           cheatBox.execute((cheatCode[0], level, cheatCode[1],
                                             cheatCode[2], cheatCode[3]))
                        if cheatCode[0] in cheatBox.getCodesByType(4) and\
                           len(cheatCode)==3:
                           cheatBox.execute((cheatCode[0], player, cheatCode[1],
                                             cheatCode[2]))

                  # Handle events on the pause menu
                  if pauseMenu.getDisplay() and not controls.getDisplay():
                     sel = pauseMenu.handleEvent(event)
                     if sel == 1:
                        if merchantLevel == None or not merchantLevel.isActive():
                           level.setActive(True)
                     if sel == 2:
                        SOUNDS.toggleMute()
                     if sel == 3:
                        tutorial.display()
                     if sel == 4:
                        controls.display()
                     if sel == 5:
                        RUNNING = False
                     

                  # Handle events for the controls menu
                  if controls.getDisplay():
                     controls.handleEvent(event)
                     if not controls.getDisplay():
                        # Allow the controls menu to be
                        # taken off the screen
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
          # Fade out the music
          SOUNDS.fadeOut(1000)
          merch = code[1]
          merchantLevel = MerchantLevel(player, merch)
          code = None

           # Reset the movement dictionary for the player
          for k in player._movement.keys():
             player._movement[k] = False

          # Display the loading screen
          loading.setDisplay(True)

      # Set Game Mode to Main Game
      elif code != None and code[0] == 0:
          SOUNDS.fadeOut(1000)
          level.setActive(True)
          code = None

          # Display the loading screen
          loading.setDisplay(True)

      # Set Game Mode to Combat
      elif code != None and code[0] == 2:
         level.setActive(False)
         SOUNDS.fadeOut(1000)
         combatLevel = CombatLevel(code[1], code[2])
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
         SOUNDS.fadeOut(1000)
         endScreen = EndScreen(player)
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

