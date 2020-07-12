import pygame
from .box import Box
from graphics.linkedprogressbar import LinkedProgressBar
from graphics.textbox import TextBox
#from graphics import LinkedProgressBar, TextBox
from rectmanager import getRects

class CombatSprite(object):

    def __init__(self,animal,position,font,enemies = False):
        """
        This class creates the combat sprites which includes:
        animal sprite
            animal health linked progress bar
            animal health
        animal name

        We also draw everything based on the input position that is given.

        Also enemies must be set to True so the sprites are flipped in the
        right direction for the combat GUI. 
        """
        self._animal = animal
        self._position = position
        self._animal_xPos = self._position[0] + 50 - (self._animal.getWidth()//2)
        self._animal_yPos = self._position[1] + 52 - (self._animal.getHeight()//2)
        self._enemies = enemies
        # makes the linked progress bar
        self._bar = LinkedProgressBar(self._animal,(self._position[0],self._position[1]+90),100,
                                      100,self._animal.getHealth())
        
        # makes the text box for animal name
        self._nameText = TextBox(self._animal.getName(),
                                 (0,0),
                                 font,(255,255,255))

        x = self._nameText.getWidth()
        self._nameText.setPosition((self._position[0]+50-(x//2),self._position[1]+107))
        healthFont = pygame.font.SysFont("Times New Roman", 12)
        
        # makes the text box for the health which will be drawn on top of health linked
        # progress bar
        self._healthText = TextBox(str(self._animal.getHealth()) + "/100",
                                   (0,0),
                                   healthFont,(255,255,255))
        x = self._healthText.getWidth()
        self._healthText.setPosition((self._position[0]+50-(x//2),self._position[1]+90))

        # sets up the collide rects
        self._collideRects = getRects(self.getAnimalSprite())

        self._box = Box(self.getPosition(),(100,107+self.getTextHeight()),(255,255,0),3)
        self._isSelected = False

    def draw(self,screen):
        """
        This methods draws the combat sprites. 
        """
        self._bar.draw(screen)
        self._nameText.draw(screen)
        self._healthText.draw(screen)
        if self._isSelected:
            self._box.draw(screen)
        if not self._enemies:
            screen.blit(self._animal.getDefaultImage(),(self._animal_xPos,self._animal_yPos))
        else:
            img = pygame.transform.flip(self._animal.getDefaultImage(), True, False)
            screen.blit(img,(self._animal_xPos,self._animal_yPos))

    def update(self,ticks):
        self.getHealthBar().update()
        self.getHealthText().setText(str(self.getAnimal().getHealth()) + "/100")

    def select(self):
        self._isSelected = True

    def deselect(self):
        self._isSelected = False

    def getHealthBar(self):
        """
        Returns the health bar of the animal. This is a linked progress bar. 
        """
        return self._bar

    def getHealthText(self):
        """
        Returns the text box item that is the health text
        """
        return self._healthText

    def getAnimal(self):
        """
        Returns the animal.
        """
        return self._animal

    def isEnemy(self):
        """
        Returns the boolean if the combat sprite belongs to the enemies.
        """
        return self._enemies

    def getAnimalSprite(self):
        """
        Return the animal sprite.
        """
        return self._animal.getDefaultImage()

    def getPosition(self):
        """
        Returns the position of the combat sprite.
        """
        return self._position

    def getAnimalPosition(self):
        """
        Returns the animal's sprite position.
        """
        return (self._animal_xPos,self._animal_yPos)

    def getCollideRects(self):
        """
        Returns the collide rects
        """
        return self._collideRects

    def getTextHeight(self):
        """
        Returns the height of the name text. 
        """
        return self._nameText.getHeight()
