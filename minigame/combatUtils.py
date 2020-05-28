"""
In this file we create the functions/classes used for the combat game.

We define a useful dictionary attackDamage that holds the amount of damage
for a combat attack sequence. 

The following functions are created:
attack
attackComputation
fortify
heal
retreat
move
lootItems
retreatLostAcorns
retreatItemLost

The following classes are created:
CombatSprite
Box
AnimalStats
RetreatScreen
"""

from items.items import *
import pygame, random, math, copy
from rectmanager import getRects
from economy.acorn import Acorn
from minigame.threexthreeinventory import threeXthreeInventory
from minigame.itemblock import ItemBlock
from graphics.linkedprogressbar import LinkedProgressBar
from graphics.textbox import TextBox
from graphics.scrollbox import ScrollBox
from graphics.scrollselector import ScrollSelector
from graphics.happinessface import HappinessFace
from graphics.popup import Popup
from graphics.button import Button
##from graphics.popupwindow import PopupWindow
from graphics.tabs import Tabs
from graphics.particletext import ParticleText
from graphics.mysurface import MySurface
##from graphics.guiUtils import ItemCard
##from player import Player


attackDamage = {(0.0,1):0,(0.25,1): 5, (0.5,1): 10, (0.75,1): 20, (1,1): 30,
                (1.25,1): 33, (1.5,1): 35, (1.75,1): 40, (2,1): 45, (2.25,1): 47,
                (2.5,1): 50, (2.75,1): 70, (3,1): 90}

"""
*Had to move over the ItemCard and makeMultiLineTextBox class the import statement would
not work properly.
"""

def makeMultiLineTextBox(text, position, font, color, backgroundColor):
    """
    Used to create multiline text boxes which are not native to
    pygame.  The user supplies the same information to this function
    that they would supplied to the TextBox Class. The function will
    split the text along new-lines and return a MySurface object
    containing all of the text formatted as desired.
    """
    lines = text.split("\n")
    width = TextBox(max(lines, key=len),position, font, color).getWidth() + 10
    height = font.get_height()
    surf = pygame.Surface((width,height*len(lines)))
    surf.fill(backgroundColor)
    p = (0,0)
    for line in lines:
        t = TextBox(line, p, font, color)
        center = width // 2 - t.getWidth() // 2
        t.setPosition((center, t.getY()))
        t.draw(surf)
        p = (0, p[1] + height)
    return MySurface(surf, position)

class ItemCard(object):

    def __init__(self, item,position = (471,166),scrollBoxSize = (155,300)):
        """
        Creates an item card for the object, this works for both items and GUIs.

        Defaults is set for the merchant GUI which needs to be changed.
        """
        self._item = item
        self._card = self.generate(item,position,scrollBoxSize)

    def getItem(self):
        """
        Returns the item that the item card is representing
        """
        return self._item

    def getCard(self):
        """
        Returns the scorllbox that is the item. 
        """
        return self._card

    def generate(self,entity, position,scrollBoxSize):
        """
        Generates the item that is the in the item card.
        """
        nameFont = pygame.font.SysFont("Times New Roman", 32)
        detailsFont = pygame.font.SysFont("Times New Roman", 16)
        s = pygame.Surface((200,600))
        s.fill((0,0,0))
        a = copy.copy(entity)
        a.setWorldBound(False)
        a.setPosition((10,50))
        if a.isFlipped():
            a.flip()
        a.scale(4)
        TextBox(a.getName(), (10,10), nameFont, (255,255,255)).draw(s)
##        if issubclass(type(entity), Animal) or issubclass(type(entity), Item): 
        a.draw(s)
        makeMultiLineTextBox(str(a), (10,200), detailsFont,
                             (255,255,255), (0,0,0)).draw(s)
        s = MySurface(s)
        return ScrollBox(position, scrollBoxSize, s, borderWidth=2)

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
    Calculates the damage dealt between an attacker and a defender.
    """
    attacker.resetDefenseModifers()
    # try/catch needed as animal equipped weapon/armor might be None
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

def lootItems(opponents):
    """
    Generates a list of items that can be used
    """
    lootItems = list()
    for x in opponents:
        if x != None:
            ivt = x.getInventory()
            for y in ivt:
                if random.randint(0,100) <= 100:#25: # items can be looted only 25% of time
                    lootItems.append(y)
    return lootItems
        
def lootAcorns(opponents):
    """
    Generates the number of acorns you looted.
    """
    acorns = sum([x.getAcorns() for x in opponents if x!=None])
    acornsLooted = acorns*random.uniform(0,0.4)
    return math.floor(acornsLooted)

def retreatLostAcorns(animal):
    """
    Acorns lost for retreating from a battle
    """
    return math.ceil(animal.getAcorns()*random.uniform(0,0.5))
     
def retreatItemLost(animal):
    """
    Chance of item lost from retreating from battle.
    """
    if 10 <= random.randint(0,100) and len(animal.getInventory()) != 0:
        item = random.choice(animal.getInventory())
        return item
    else:
        return None
    
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

    def draw(self,screen):
        """
        This methods draws the combat sprites. 
        """
        self._bar.draw(screen)
        self._nameText.draw(screen)
        self._healthText.draw(screen)
        if not self._enemies:
            screen.blit(self._animal.getDefaultImage(),(self._animal_xPos,self._animal_yPos))
        else:
            img = pygame.transform.flip(self._animal.getDefaultImage(), True, False)
            screen.blit(img,(self._animal_xPos,self._animal_yPos))

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
        Will draw the box on the combat minigame gui.
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
        stats as well as other useful stats for combat. This is created
        when the animal sprite is right clicked on.

        It displays the animal's name, health, acorns, inventory,
        happiness face, and an exit button to close the screen.
        """
        # self._y is used throughout to get good height spacing
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
        # the happiness face text
        self._opinionText = TextBox("Opinion: ",(self._xpos,self._ypos+text_y+\
                                                 8),
                                    self._font,(255,255,255))
        x = self._opinionText.getWidth()
        # checks to see if class is player so no happiness face is drawn
        if str(type(self._animal)) == "<class 'player.Player'>":
            self._opinionText.setText("Opinion: --")
            text_y += self._opinionText.getHeight() + 11
        # creates the happiness face
        else:
            self._opinion = HappinessFace((self._xpos + x,self._ypos+text_y+2))
            self._opinion.setFace(self._animal.getFriendScore())
            text_y += self._opinion.getHeight()

        # the health text
        self._healthtext = TextBox("Health: "+str(self._animal.getHealth())+\
                                   "/100",
                                   (self._xpos,self._ypos+text_y+2),self._font,
                                   (255,255,255))
        text_y += self._healthtext.getHeight()
        # the acorns text
        self._acornsText = TextBox("Acorns: "+str(self._animal.getAcorns()),
                                   (self._xpos,self._ypos+text_y+6),self._font,
                                   (255,255,255))
        x = self._acornsText.getWidth()
        self._acornImg = Acorn((self._xpos+x,self._ypos+text_y+2))

        # Exit Button
        self._exitButton = Button("X",(self._xpos + 400,self._ypos),
                                  self._font,(0,0,0),(100,100,100),25,25,
                           (0,0,0), 1)

        # Inventory Items
        text_y += self._acornsText.getHeight() + 10
        x = self._healthtext.getWidth()
        # weapon text 
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen = self._weaponText.getWidth()
        # draws item block that will have the weapon
        self._weapon = ItemBlock((self._xpos+xlen+5,self._ypos+text_y+10),(50,50), item=self._animal.getEquipItem())
        self._weaponText = TextBox("Weapon equipped: ",(self._xpos,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        # armor text
        self._armorText = TextBox("Armor equipped: ",(self._xpos+xlen+75,self._ypos+text_y+10),
                                   self._font,(255,255,255))
        xlen += self._armorText.getWidth()
        # draws item block that will have the armor
        self._armor = ItemBlock((self._xpos+xlen+80,self._ypos+text_y+10),(50,50), item=self._animal.getArmor())
        # Sets up inventory display screen
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
        Draws the interface onto the combat screen
        """
        if self._display == True:
            self._name.draw(screen)
            if str(type(self._animal)) == "<class 'player.Player'>":
                self._opinionText.draw(screen)
            else:
                self._opinionText.draw(screen)
                self._opinion.draw(screen)
            self._exitButton.draw(screen)
            self._healthtext.draw(screen)
            self._acornsText.draw(screen)
            self._acornImg.draw(screen)
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
        """
        Updates the text based on any changes in animal health or acorns.
        """
        self._healthtext.setText("Health: "+str(self._animal.getHealth())+\
                                   "/100")
        self._acornsText.setText("Acorns: "+str(self._animal.getAcorns()))

class RetreatScreen(object):

    def __init__(self,player):
        """
        In this class we create the retreat screen that the player sees when
        they click the retreat button

        The screen consists of:

        The numbers of acorns the player lost

        Displays the inventory along with items lost
        """
        self._player = player
        # calculates the number of acorns lost
        self._moneyLost = retreatLostAcorns(self._player)
        player.setAcorns(self._player.getAcorns()-self._moneyLost)

        self._font = pygame.font.SysFont("Times New Roman", 20)
        # calculates the number of items lost
        self._itemLost = retreatItemLost(self._player)
        if self._itemLost != None:
            self._player.getInventory().removeItem(self._itemLost)

        # the text that is displayed in the screen
        self._lostMoneyText = TextBox("You lost "+ str(self._moneyLost) + " acorns.",
                                      (0,0),self._font,(255,255,255))
        x = self._lostMoneyText.getWidth()
        self._lostMoneyText.setPosition((600-(x//2),150))
        y = self._lostMoneyText.getHeight()
        if self._itemLost != None:
            self._itemLostText = TextBox("You lost your " + self._itemLost.getName(),
                                         (0,0),self._font,(255,255,255))
            x = self._itemLostText.getWidth()
            self._itemLostText.setPosition((600-(x//2),150+y+5))
            y += self._itemLostText.getHeight()
        self._inventoryText = TextBox("Your inventory: ",(450,150+y+20),
                                     self._font,(255,255,255))

        self._acornsText = TextBox("Acorns: "+str(self._player.getAcorns()),
                                   (0,0),self._font,
                                   (255,255,255))
##        self._acornImg = Acorn((0,0))
        self._acornsText.setPosition((750-(self._acornsText.getWidth()+5),150+y+20))
        #self._acornImg.setPosition((750-self._acornImg.getWidth(),150+y+15))
        y += self._acornsText.getHeight() + 20
        self._inventory = threeXthreeInventory((450,150+y+5),(300,200), self._player)
        
    def draw(self,screen):
        """
        We draw the retreat screen to the screen.
        """
        self._lostMoneyText.draw(screen)
        if self._itemLost != None:
            self._itemLostText.draw(screen)
        self._acornsText.draw(screen)
##        self._acornImg.draw(screen)
        self._inventoryText.draw(screen)    
        self._inventory.draw(screen)
        
