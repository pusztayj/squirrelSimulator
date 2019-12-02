"""
In this file we create the functions/classes used for the combat game.
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

def lootItems(opponents):
    """
    Generates a list of items that can be used
    """
    lootItems = list()
    for x in opponents:
        if x != None:
            ivt = x.getInventory()
            for y in ivt:
                if random.randint(0,100) <= 100: # items can be looted only 75% of time
                    lootItems.append(y)
    return lootItems
        
def lootAcorns(opponents):
    """
    Generates the number of acorns you looted.
    """
    acorns = sum([x.getAcorns() for x in opponents if x!=None])
    acornsLooted = acorns*random.uniform(.25,1)
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
        self._animal = animal
        self._position = position
        self._animal_xPos = self._position[0] + 50 - (self._animal.getWidth()//2)
        self._animal_yPos = self._position[1] + 52 - (self._animal.getHeight()//2)
        self._enemies = enemies
        self._bar = LinkedProgressBar(self._animal,(self._position[0],self._position[1]+90),100,
                                      100,self._animal.getHealth())
        self._nameText = TextBox(self._animal.getName(),
                                 (0,0),
                                 font,(255,255,255))

        x = self._nameText.getWidth()
        self._nameText.setPosition((self._position[0]+50-(x//2),self._position[1]+107))
        healthFont = pygame.font.SysFont("Times New Roman", 12)
        self._healthText = TextBox(str(self._animal.getHealth()) + "/100",
                                   (0,0),
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
        if str(type(self._animal)) == "<class 'player.Player'>":
            self._opinionText.setText("Opinion: --")
            text_y += self._opinionText.getHeight() + 11
        else:
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
        self._acornImg = Acorn((self._xpos+x,self._ypos+text_y+2))

        # Exit Button
        self._exitButton = Button("X",(self._xpos + 400,self._ypos),
                                  self._font,(0,0,0),(100,100,100),25,25,
                           (0,0,0), 1)

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
        self._healthtext.setText("Health: "+str(self._animal.getHealth())+\
                                   "/100")
        self._acornsText.setText("Acorns: "+str(self._animal.getAcorns()))


class VictoryScreen(object):

    def __init__(self,dead,player):
        self._dead = dead
        self._player = player

        # acorns looted
        self._lootedAcorns = lootAcorns(self._dead)

        # graphics settings
        self._FLAG = True
        self._itemCard = None

        self._addedAcorns = False
        
        # fonts
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        self._font = pygame.font.SysFont("Times New Roman", 16)

        # needed text boxes
        text = "Congratuations! You defeated your enemies."
        self._victoryText = TextBox(text,(100,25),self._textFont,(255,255,255))
        y = self._victoryText.getHeight()
        self._acornLooted = TextBox("Acorns Looted: "+str(self._lootedAcorns),
                                    (100,25+y+2),self._textFont,(255,255,255))
        y += self._acornLooted.getHeight()
        self._acornCount = TextBox("Your Acorns: "+str(self._player.getAcorns()+self._lootedAcorns),
                                   (100,25+y+2),self._textFont,(255,255,255))
        y += self._acornCount.getHeight()

        # tabs
        self._tabs = Tabs(["Pickup","Drop"], (100,25+y+5), self._font, (0,0,0), (255,255,255), (200,50),
               (0,0,0),(255,255,255))
        y += self._tabs.getHeight()
        
        # items looted
        self._lootedItems = lootItems(self._dead)
        self._lootItems = [{"text": item.getName(),"func": self.selectItem,"args":item} \
                      for item in self._lootedItems]
        self._lootedItemSelect = ScrollSelector((100,25+y+10),(250,300),30,self._lootItems,(0,0,0))

        # player items
        self._player_items = [{"text": item.getName(),"func": self.selectItem,"args":item} \
                      for item in self._player.getInventory()]
        self._playerSelect = ScrollSelector((100,25+y+10),(250,300),30,self._player_items,(0,0,0))
        self._y = y

        self._executePickUp = Button("Pick up Item",(450,self._y+25-50),
                                         self._font,(255,255,255),(34,139,34),48,140,borderWidth = 2)

        self._executeDrop = Button("Drop Item",(450,self._y+25-50),
                                         self._font,(255,255,255),(34,139,34),48,140,borderWidth = 2)

        self._cancelTransaction = Button("Cancel Transaction",(450+156,self._y+25-50),
                                         self._font,(255,255,255),(207,51,17),48,140,borderWidth = 2)

    def selectItem(self,item):
        self._itemCard = ItemCard(item, position = (450,self._y+25+10), scrollBoxSize = (200,300))

    def updateDisplay(self):
        if self._tabs.getActive() == 0:
            return True
        else:
            return False

    def cancelTransaction(self):
        self._itemCard = None

    def pickUpItem(self,item):
        self._player.getInventory().addItem(item)
        self._lootedItems.remove(item)
        
    def draw(self,screen):
        if not self._addedAcorns:
            self._player.setAcorns(self._player.getAcorns()+self._lootedAcorns)
            self._addedAcorns = True
        self._victoryText.draw(screen)
        self._acornLooted.draw(screen)
        self._acornCount.draw(screen)
        if self._FLAG:
            self._lootedItemSelect.draw(screen)
        else:
            self._playerSelect.draw(screen)
        if self._itemCard != None:
            self._itemCard.getCard().draw(screen)
            self._cancelTransaction.draw(screen)
            if self._FLAG:
                self._executePickUp.draw(screen)
            else:
                self._executeDrop.draw(screen)
            
        self._tabs.draw(screen)

    def handleEvent(self,event):
        self._tabs.handleEvent(event)
        if self._FLAG:
            self._lootedItemSelect.handleEvent(event)
        else:
            self._playerSelect.handleEvent(event)
        if self._itemCard != None:
            self._itemCard.getCard().move(event)
            if self._FLAG:
                self._executePickUp.handleEvent(event,
                                    self.pickUpItem,self._itemCard.getItem())
            else:
                self._executeDrop.handleEvent(event,
                                    self._player.getInventory().removeItem,
                                              self._itemCard.getItem())
            self._cancelTransaction.handleEvent(event,
                                        self.cancelTransaction)

            self._playerSelect.updateSelections([{"text": item.getName(),"func": self.selectItem,"args":item} \
                      for item in self._player.getInventory()])
            self._lootedItemSelect.updateSelections([{"text": item.getName(),"func": self.selectItem,"args":item} \
                      for item in self._lootedItems])

    def update(self):
        if self._FLAG != self.updateDisplay():
            self._itemCard = None
        self._FLAG = self.updateDisplay()


class RetreatScreen(object):

    def __init__(self,player):
        self._player = player
        self._moneyLost = retreatLostAcorns(self._player)
        player.setAcorns(self._player.getAcorns()-self._moneyLost)

        self._font = pygame.font.SysFont("Times New Roman", 20)
        
        self._itemLost = retreatItemLost(self._player)
        if self._itemLost != None:
            self._player.getInventory().removeItem(self._itemLost)
        
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
        self._acornImg = Acorn((0,0))
        self._acornsText.setPosition((750-(self._acornsText.getWidth()+self._acornImg.getWidth()+5),150+y+20))
        self._acornImg.setPosition((750-self._acornImg.getWidth(),150+y+15))
        y += self._acornImg.getHeight() + 20
        self._inventory = threeXthreeInventory((450,150+y+5),(300,200), self._player)
        
    def draw(self,screen):
        self._lostMoneyText.draw(screen)
        if self._itemLost != None:
            self._itemLostText.draw(screen)
        self._acornsText.draw(screen)
        self._acornImg.draw(screen)
        self._inventoryText.draw(screen)    
        self._inventory.draw(screen)
        
