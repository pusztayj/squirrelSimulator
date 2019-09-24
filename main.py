
import pygame, random
##from modules.vector2D import Vector2
##from modules.orb import Orb
##from modules.star import Star
##from modules.drawable import Drawable
##from modules.textbox import TextBox

SCREEN_SIZE = (1200,800)
WORLD_SIZE  = (1200,1200)

def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()
   pygame.font.init()

   #Load in the desired font for score keeping
   font = pygame.font.SysFont("Arial", 32)

   #Store the pygame key codes for simplicity later
   movement_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

   #Update the title for the window
   pygame.display.set_caption('Project 2')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Load the background image
   background = Drawable("background.png", Vector2(0,0), transparent=False)

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   #Create a list to hold the orb objects
   orbs = []

   #Create an instance of the star class
   star = Star(Vector2(WORLD_SIZE[0]//2,WORLD_SIZE[1]//2))

   #Initialize the score to 0
   SCORE = 0

   #Create a textbox for the current score
   scoreDisplay = TextBox("Score: " + str(SCORE), (618,10), font, (255,255,255))

   #Create a textbox displaying the number of orbs on the field
   orbCountDisplay = TextBox("Orbs: " + str(len(orbs)), (630,50), font, (255,255,255))

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      background.draw(screen)

      #Draw the orb to the screen
      for orb in orbs:
         orb.draw(screen)

      #Draw the star to the screen
      star.draw(screen)

      #Draw the score display and orb count display
      scoreDisplay.draw(screen)
      orbCountDisplay.draw(screen)
      

      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         
         # close the window on QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

         # create orbs where the mouse is clicked
         elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            orbs.append(Orb(Drawable.adjustMousePos(event.pos)))

         # create 100 orbs when the scroll wheel is pressed
         elif event.type == pygame.MOUSEBUTTONDOWN and event.button==2:
            newOrbs = [Orb(Drawable.adjustMousePos(event.pos)) for x in range(100)]
            orbs += newOrbs

         star.move(event)

      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      #Update the star's position
      star.update(WORLD_SIZE, ticks)
      
      #Update the orbs' positions
      for orb in orbs:
         orb.update(WORLD_SIZE, ticks)
         #Determine which if any orbs have collided with the star
         if orb.getCollideRect().colliderect(star.getCollideRect()):
            orb.kill()

      #Update the offset based on the stars location
      star.updateOffset(star, SCREEN_SIZE, WORLD_SIZE)

      #Increment the score by the number of newly dead orbs
      SCORE += len([orb for orb in orbs if orb.isDead()])

      #Update the score board to reflect the new score
      scoreDisplay.setText("Score: " + str(SCORE))

      #Remove dead orbs from the orbs list
      orbs = [orb for orb in orbs if not orb.isDead()]

      #Update the orb count display
      orbCountDisplay.setText("Orbs: " + str(len(orbs)))

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()
