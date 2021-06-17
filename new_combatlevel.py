"""
@author: Trevor Stalnaker, Justin Pusztay
File: main.py

The main loop for running Squirrel Simulator
"""

import pygame, random, math
from minigame import *
from animals import *
from managers import CONSTANTS, USER_INTERFACE, SOUNDS
from minigame.turnOrder import TurnOrder

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

   alvin = Creature("chipmunk", name="Alvin", pos=(0,0))
   allies = Pack(alvin)
   alvin.setPack(allies)

   simon = Creature("chipmunk", name="Simon", pos=(0,0))
   allies.addMember(simon)
   simon.setPack(allies)

   theo = Creature("chipmunk", name="Theodore", pos=(0,0))
   allies.addMember(theo)
   theo.setPack(allies)

   enemy1 = Creature("fox", name="enemy1", pos=(0,0))
   enemies = Pack(enemy1, maxSize=4)
   enemy1.setPack(enemies)

   enemy2 = Creature("fox", name="enemy2", pos=(0,0))
   enemies.addMember(enemy2)
   enemy2.setPack(enemies)

   enemy3 = Creature("fox", name="enemy3", pos=(0,0))
   enemies.addMember(enemy3)
   enemy3.setPack(enemies)

##   enemy4 = Creature("fox", name="enemy4", pos=(0,0))
##   enemies.addMember(enemy4)
##   enemy4.setPack(enemies)

   to = TurnOrder(allies, enemies)
   
   npcTurnLength = 3
   npcTurnTimer = npcTurnLength

   current = None

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT):
            RUNNING = False
         if event.type == pygame.KEYDOWN and \
            event.key == pygame.K_a and \
            to.getCurrent() == alvin:
            print("Player took their turn...\n")
            to.getNext()
         if event.type == pygame.KEYDOWN and \
            event.key == pygame.K_k and \
            to.getCurrent() == alvin:
            kill = input("Who to kill..?  ")
            print("Player took their turn...\n")
            enemies.removeMember(eval(kill))
            to.getNext()
            
                      
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      if current != to.getCurrent():
         #print(to.getCurrent().getName() + "'s turn")
         current = to.getCurrent()

      if to.getCurrent() != None:
         npcTurnTimer -= ticks
         if npcTurnTimer <= 0:
            print(to.getCurrent().getName() + "'s turn")
            
            npcTurnTimer = npcTurnLength
            
            if random.random() > .6:
               if to.getCurrent() in allies.getTrueMembers():
                  killed = random.choice(enemies.getTrueMembers())
                  enemies.removeMember(killed)
               else:
                  killed = random.choice(allies.getTrueMembers())
                  allies.removeMember(killed)
               print(to.getCurrent().getName(), "killed", killed.getName())
            print("NPC turn over...\n")
            #print("New Turn Order", to.getOrder)
            to.getNext()
            
            

      if allies.isDead() or enemies.isDead():
         RUNNING = False
         print("Simulation Over")
         
                   
   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

