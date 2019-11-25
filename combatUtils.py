"""
In this file we create the functions for the combat game.
"""

from items.items import *
from graphics import *
import pygame
from rectmanager import getRects
from economy.acorn import Acorn
from minigame.threexthreeinventory import threeXthreeInventory
from minigame.itemblock import ItemBlock

attackDamage = {(0.0,1):0,(0.25,1): 5, (0.5,1): 10, (0.75,1): 20, (1,1): 30,
                (1.25,1): 33, (1.5,1): 35, (1.75,1): 40, (2,1): 45,
                (2.5,1): 50, (2.75,1): 70, (3,1): 90}

def attack(attacker, defender):
    """
    Executes an attack where one characer gives damage to another player.
    Damage dealt is calculated on a ratio of strengths. It takes a ratio
    between attacker's strength and defenders strength.

    It awards damage based on the attackdamage dictionary.
    """
    
    damage = attackComputation(attacker,defender)
    defender.loseHealth(damage)
    # potential gain xp
    # potential stamina loss

def attackComputation(attacker,defender):
    """
    Calculates the damage dealt.
    """
    attacker.resetDefenseModifers()
    try:
        attack_strength = (attacker.getStrength() + \
                               (attacker.getEquipItem().getStrength())) * \
                               attacker.getAttackModifers()
    except AttributeError:
        attack_strength = attacker.getStrength()*attacker.getAttackModifers()

    try:
        defense_strength = (defender.getStrength() + \
                           (defender.getArmor().getStrength())) * \
                           defender.getDefenseModifers()
    except AttributeError:
        defense_strength = defender.getStrength()*defender.getDefenseModifers()
                         
    ratio = (round((attack_strength/defense_strength) * 4))/ 4
    if ratio > 3:
        damage = 95
    else:
        damage = attackDamage[(ratio,1)]
    return damage

def fortify(animal):
    """
    Fortifies an animal by increasing their defensive strength by 25%. Also
    heals animal by 10 points.
    """
    animal.heal(10)
    animal.addDefenseModifers(.25)

def heal(animal,potion):
    """
    Heals the animal based on the health potion.
    """
    animal.resetDefenseModifers()
    if potion in animal.getInventory():
        animal.getInventory().removeItem(potion)
        animal.heal(potion.getHealthBoost())
    else:
        return "You cannont heal"

def retreat(animal):
    """
    Forces an animal to retreat
    """
    animal.resetDefenseModifers()

def move(animal,opponents):
    """
    Tests the animal logic so the NPC can decide their move.
    """
    if animal.healLogic(opponents):
        potions = [x for x in animal.getInventory() if type(x) == type(Potions())]
        potions.sort(key = lambda x: x.getHealthBoost())
        if len(potions) != 0:
            heal(animal,potions[-1])
    elif animal.fortifyLogic(opponents):
        fortify(animal)
    else:
        an = animal.attackLogic(opponents)
        attack(animal,an)
    
class CombatSprite(object):

    def __init__(self,animal,position,font,enemies = False):
        self._animal = animal
        self._position = position
        self._animal_xPos = self._position[0] + 50 - (self._animal.getWidth()//2)
        self._animal_yPos = self._position[1] + 52 - (self._animal.getHeight()//2)
        self._enemies = enemies
        self._bar = LinkedProgressBar(self._animal,(self._position[0],self._position[1]+90),100,
                                      100,self._animal.getHealth())
        self._nameText = TextBox(self._animal.getName(),
                                 (self._position[0],self._position[1]+107),
                                 font,(255,255,255))

        x = self._nameText.getWidth()
        self._nameText.setPosition((self._position[0]+50-(x//2),self._position[1]+107))
        healthFont = pygame.font.SysFont("Times New Roman", 12)
        self._healthText = TextBox(str(self._animal.getHealth()) + "/100",
                                   (self._position[0],self._position[1]+125),
                                   healthFont,(255,255,255))
        x = self._healthText.getWidth()
        self._healthText.setPosition((self._position[0]+50-(x//2),self._position[1]+90))
        self._collideRects = getRects(self.getAnimalSprite())

    def draw(self,screen):
        self._bar.draw(screen)
        self._nameText.draw(screen)
        self._healthText.draw(screen)
        if not self._enemies:
            screen.blit(self._animal.getDefaultImage(),(self._animal_xPos,self._animal_yPos))
        else:
            img = pygame.transform.flip(self._animal.getDefaultImage(), True, False)
            screen.blit(img,(self._animal_xPos,self._animal_yPos))

    def getHealthBar(self):
        return self._bar

    def getHealthText(self):
        return self._healthText

    def getAnimal(self):
        return self._animal

    def isEnemy(self):
        return self._enemies

    def getAnimalSprite(self):
        return self._animal.getDefaultImage()

    def getPosition(self):
        return self._position

    def getAnimalPosition(self):
        return (self._animal_xPos,self._animal_yPos)

    def getCollideRects(self):
        return self._collideRects

    def getTextHeight(self):
        return self._nameText.getHeight()


class Box(object):

    def __init__(self,position,demensions,color,width):
        """
        Here we create a box. It needs a position and a demension
        to create a box that is not filled in with those demensions.
        You can also input the color and the width (thickness) of the
        lines. 
        """
        self._position = position
        self._demensions = demensions
        self._x = self._demensions[0]
        self._y = self._demensions[1]
        self._width = width
        self._color = color

    def draw(self,screen):
        """
        Will draw the box on the input screen.
        """ 
        pygame.draw.line(screen,self._color,(self._position[0],self._position[1]),
                         (self._position[0],self._position[1]+self._y),
                         self._width)
        pygame.draw.line(screen,self._color,self._position,
                         (self._position[0]+self._x,self._position[1]),
                         self._width)       
        pygame.draw.line(screen,self._color,(self._position[0],self._position[1]+self._y),
        (self._position[0]+self._x,self._position[1]+self._y),
        self._width)
        pygame.draw.line(screen,self._color,(self._position[0]+self._x,self._position[1]),
                         (self._position[0]+self._x,self._position[1]+self._y),
                         self._width)

    def setPosition(self,newPosition):
        """
        Sets a new position to the box.
        """
        self._position = newPosition


class AnimalStats(object):

    def __init__(self,animal,position):
        """
        Creates an animal display for the user to see. It shows relevant
        stats as well as other useful stats for combat.
        """
        self._display = True
        self._animal = animal
        self._position = position
        self._xpos = self._position[0]
        self._ypos = self._position[1]
        self._font = pygame.font.SysFont("Times New Roman", 18)
        # Text Stat display along with appropriate images
        self._name = TextBox("Name: " + self._animal.getName(),self._position,
                             self._font,(255,255,255))
        text_y = self._name.getHeight()
        self._opinionText = TextBox("Opinion: ",(self._xpos,self._ypos+text_y+\
                                                 8),
                                    self._font,(255,255,255))
        x = self._opinionText.getWidth()
        self._opinion = HappinessFace((self._xpos + x,self._ypos+text_y+2))
        self._opinion.setFace(self._animal.getFriendScore())

        text_y += self._opinion.getHeight()
        self._healthtext = TextBox("Health: "+str(self._animal.getHealth())+\
                                   "/100",
                                   (self._xpos,self._ypos+text_y+2),self._font,
                                   (255,255,255))
        text_y += self._healthtext.getHeight()
        self._acornsText = TextBox("Acorns: "+str(self._animal.getAcorns()),
                                   (self._xpos,self._ypos+text_y+6),self._font,
                                   (255,255,255))
        x = self._acornsText.getWidth()
        self._acormImg = Acorn((self._xpos+x,self._ypos+text_y+2))

        # Exit Button
        self._exitButton = Button("X",(self._xpos + 400,self._ypos),
                                  self._font,(0,0,0),(100,100,100),25,25,
                           (0,0,0), 1)
        #x = self._exitButton.getWidth()
        self._exitButton.setPosition((self._xpos + 400,self._ypos))

        # Inventory Items
        text_y += self._acornsText.getHeight() + 10
        x = self._healthtext.getWidth()
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen = self._weaponText.getWidth()
        self._weapon = ItemBlock((self._xpos+xlen+5,self._ypos+text_y+10),(50,50), item=self._animal.getEquipItem())
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        self._armorText = TextBox("Armor equipped: ",(self._xpos+xlen+75,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen += self._armorText.getWidth()
        self._armor = ItemBlock((self._xpos+xlen+80,self._ypos+text_y+10),(50,50), item=self._animal.getArmor())
        self._inventory = threeXthreeInventory((self._xpos+x+30,self._ypos),(xlen-14,text_y), self._animal)

    def getDisplay(self):
        """
        Returns the display boolean.
        """
        return self._display
        
    def close(self):
        """
        This method closes the stats window.
        """
        self._display = False

    def draw(self,screen):
        """
        Draws the window.
        """
        if self._display == True:
            self._name.draw(screen)
            self._opinionText.draw(screen)
            self._opinion.draw(screen)
            self._exitButton.draw(screen)
            self._healthtext.draw(screen)
            self._acornsText.draw(screen)
            self._acormImg.draw(screen)
            self._inventory.draw(screen)
            self._weaponText.draw(screen)
            self._weapon.draw(screen)
            self._armorText.draw(screen)
            self._armor.draw(screen)

    def handleEvent(self,event):
        """
        Handles how the user interacts with the window.
        """
        self._exitButton.handleEvent(event, self.close)

    def update(self):
        self._healthtext.setText("Health: "+str(self._animal.getHealth())+\
                                   "/100")
        self._acornsText.setText("Acorns: "+str(self._animal.getAcorns()))
    
