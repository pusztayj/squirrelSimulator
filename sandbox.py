"""
@author: Trevor Stalnaker, Justin Pusztay
File: main.py

The main loop for running Squirrel Simulator
"""

import pygame, random, math, os, copy
from minigame import *
from minigame.world.utils import PackManager
from polybius.graphics import *
from graphics.tradeMenu import TradeMenu
from player import Player
from items.item import Item
##from economy.merchant import Merchant
from animals import *
from polybius.managers import CONSTANTS, SOUNDS, FRAMES
from managers import ANIMALS, NAMES, ITEMS, USER_INTERFACE
##from event import EventWrapper

USER_INTERFACE.setResourcePath(os.path.join("resources","data","menuButtons.csv"))

FRAMES.prepareImagesFromCSV(os.path.join("resources","data","images.csv"),
                               os.path.join("resources","images"))

CONSTANTS.setResourcePath(os.path.join("resources","data","constants.csv"))

NAMES.setResourcePath(os.path.join("resources","data","names.csv"))
ITEMS.setResourcePath(os.path.join("resources","data","items.csv"))
ANIMALS.setResourcePath(os.path.join("resources","data","animals.csv"))
SCREEN_SIZE = CONSTANTS.get("screen_size")

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

   font = pygame.font.SysFont("Times New Roman", 20)

   font2 = pygame.font.SysFont("Time New Roman", 40)

   menuType = ""

   c1 = Creature("deer")
   c2 = Creature("bear")
   c3 = Creature("deer")

   pack = Pack(c1)
   pack.addMember(c2)
   pack.addMember(c3)

   c1.setPack(pack)
   c2.setPack(pack)
   c3.setPack(pack)

   i = Item("sword", c1)

   c1.getInventory().addItem(i)
   c1.getInventory().addItem(Item("nutsoup", c2))

   c2.getInventory().addItem(Item("sword", c1))
   c2.getInventory().addItem(Item("nutsoup", c2))

##   inv = threeXthreeInventory((150,150), (200,200), c1)
##   inv2 = threeXthreeInventory((500,150), (200,200), c2)
##
##   invs = [inv, inv2]

   packManager = PackManager(pack, SCREEN_SIZE)

   tm = TradeMenu((50,50), (1050, 400), c1, c2, i)
   tm.center()

   inc = Incrementer((100,100),
                     padding=(10,10), defaultValue=0,
                     minValue=-10,maxValue=10,activeTextInput=False
                     ,buttonText=["-","+"], increments=[1],
                     buttonBorderWidth=2, buttonDims=(15,20),
                     valueBoxBorderWidth=0,valueBoxBackgroundColor=None,
                     valueBoxAntialias=False,valueFont=font2)
   inc.center(cen_point=(1/2,7/8))

   # Combat buttons formated as a menu
##   item_commands = USER_INTERFACE.getControlsForMenu("playerItemManagement")
##   itemMenu = Menu((385,100),(120, 100), item_commands, padding=(4,3), spacing=2,
##                     color=(120,120,120), borderWidth=0, orientation="vertical")
##
##   item_commands2 = USER_INTERFACE.getControlsForMenu("packItemManagement")
##   itemMenu2 = Menu((685,100),(120, 100), item_commands2, padding=(4,3), spacing=2,
##                     color=(120,120,120), borderWidth=0, orientation="vertical")
##
##   item_commands3 = USER_INTERFACE.getControlsForMenu("playerItemBorrowedManagement")
##   itemMenu3 = Menu((385,250),(120, 100), item_commands3, padding=(4,3), spacing=2,
##                     color=(120,120,120), borderWidth=0, orientation="vertical")
##
##   item_commands4 = USER_INTERFACE.getControlsForMenu("packItemBorrowedManagement")
##   itemMenu4 = Menu((685,250),(120, 100), item_commands4, padding=(4,3), spacing=2,
##                     color=(120,120,120), borderWidth=0, orientation="vertical")


   itemMenu = None

   dropDownTemplate = USER_INTERFACE.getControlsForMenu("dropDownTemplate")[0]
   dropdown = None

   # Really nice blue: (34,67,120)


   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      screen.fill((255,255,255))

##      for i in invs:
##         i.draw(screen)

      packManager.draw(screen)
##
##      if tm != None and tm.getDisplay():
##         tm.draw(screen)

##      inc.draw(screen)

      if itemMenu != None:
         itemMenu.draw(screen)

      if dropdown != None:
         dropdown.draw(screen)

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT):
            RUNNING = False

##         tm.handleEvent(event)

         if itemMenu != None:
            
            e = itemMenu.handleEvent(event)

            # Create the dropdown for sharing and gifting items
            if e in (1, 2) and menuType=="playerItem":

               # Find the position of the new dropdown
               dropdown_y = itemMenu.getButtonByPosition(e-1).getY()
               dropdown_x = itemMenu.getX() + itemMenu.getWidth()

               # Create the commands for the new dropdown
               dropdown_commands = []
               for an in pack.getTrueMembers():
                  if an != pack.getLeader():
                     temp = copy.copy(dropDownTemplate)
                     temp["text"] = an.getName()
                     dropdown_commands.append(temp)

               # Create the new menu
               i = len(dropdown_commands)
               if i > 0:
                  dropDownHeight = 2 + (2*(i-1)) + (23*i)
                  dropdown = Menu((dropdown_x,dropdown_y),(120, dropDownHeight),
                                  dropdown_commands, padding=(1,1), spacing=2,
                                  color=(120,120,120), borderWidth=0, orientation="vertical")

            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
               if not itemMenu.getCollideRect().collidepoint(mouse_pos) and \
               (dropdown == None or not dropdown.getCollideRect().collidepoint(mouse_pos)):
                  itemMenu = None
                  dropdown = None


            if e == 1:
               if menuType == "playerItem":
                  dropType = "share"
               elif menuType == "itemBorrowedByPlayer":
                  print("return")
               elif menuType == "itemBorrowedByPack":
                  print("reclaim")
               elif menuType == "packItem":
                  print("borrow")

            if e == 2:
               if menuType == "playerItem":
                  dropType = "gift"
               elif menuType == "itemBorrowedByPlayer":
                  print("request ownership")
               elif menuType == "itemBorrowedByPack":
                  print("give ownership")
               elif menuType == "packItem":
                  print("request ownership")
            if e == 3:
               if menuType == "playerItem":
                  print("trade")
               elif menuType == "itemBorrowedByPlayer":
                  print("trade")
               elif menuType == "itemBorrowedByPack":
                  print("trade")
               elif menuType == "packItem":
                  print("trade")
            if e == 4:
               if menuType == "playerItem":
                  print("item stats")
               elif menuType == "itemBorrowedByPlayer":
                  print("item stats")
               elif menuType == "itemBorrowedByPack":
                  print("item stats")
               elif menuType == "packItem":
                  print("item stats")
     
##         for inventory in invs:
##            
##            item = inventory.handleEvent(event)
##            if item != None:
##               
##               mouse_pos = pygame.mouse.get_pos()
##
##               owner = item.getAttribute("owner")
##               if owner == c1 and inventory.getEntity() == c1:
##                  item_commands = USER_INTERFACE.getControlsForMenu("playerItemManagement")
##                  menuType = "playerItem"
##               elif owner != c1 and inventory.getEntity() == c1:
##                  item_commands = USER_INTERFACE.getControlsForMenu("playerItemBorrowedManagement")
##                  menuType = "itemBorrowedByPlayer"
##               elif owner == c1 and inventory.getEntity() != c1:
##                  item_commands = USER_INTERFACE.getControlsForMenu("packItemBorrowedManagement")
##                  menuType = "itemBorrowedByPack"
##               elif owner != c1 and inventory.getEntity() != c1:
##                  item_commands = USER_INTERFACE.getControlsForMenu("packItemManagement")
##                  menuType = "packItem"
##                  
##               itemMenu = Menu(mouse_pos,(120, 102), item_commands, padding=(4,3), spacing=2,
##                        color=(120,120,120), borderWidth=1, orientation="vertical")

         if dropdown != None:

            # Remove the dropdown if the mouse moves away
            mouse_pos = pygame.mouse.get_pos()
            if not itemMenu.getCollideRect().collidepoint(mouse_pos) and \
               not dropdown.getCollideRect().collidepoint(mouse_pos):
               dropdown = None
            
            de = dropdown.handleEvent(event)
            if de != None:
               creature = [an for an in pack.getTrueMembers() if not an == pack.getLeader()][de-1]
               print(dropType, creature.getName())
               dropdown = None
               itemMenu = None

         packManager.handleEvent(event)

         inc.handleEvent(event)



             
            
      #Calculate ticks
      ticks = gameClock.get_time() / 1000
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

