"""
In this file we create the functions for the combat game.
"""

from items.items import *
from graphics import *
import pygame
from rectmanager import getRects

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
        #print(type(defender))
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
                                 (self._position[0],self._position[1]+105),
                                 font,(255,255,255))
        x = self._nameText.getWidth()
        self._nameText.setPosition((self._position[0]+50-(x//2),self._position[1]+105))
        self._collideRects = getRects(self.getAnimalSprite())

    def draw(self,screen):
        self._bar.draw(screen)
        self._nameText.draw(screen)
        if not self._enemies:
            screen.blit(self._animal.getDefaultImage(),(self._animal_xPos,self._animal_yPos))
        else:
            img = pygame.transform.flip(self._animal.getDefaultImage(), True, False)
            screen.blit(img,(self._animal_xPos,self._animal_yPos))

    def getHealthBar(self):
        return self._bar

    def getAnimal(self):
        return self._animal

    def isEnemy(self):
        return self._enemies

    def getAnimalSprite(self):
        return self._animal.getDefaultImage()

    def getPosition(self):
        return (self._animal_xPos,self._animal_yPos)

    def getCollideRects(self):
        return self._collideRects

