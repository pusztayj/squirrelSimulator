"""
@authors: Justn Pusztay, Trevor Stalnaker

In this file we abstract the characteristics for each animal that
is shared by each NPC and the player. We include traits such as
health, stamina, xp, and strength. We also keep an inventory for the animal
along with the acorns that the animal can have. We also keep track of the
hunger of the animal in this class.

We also include the logic for the animal when it comes to buying and selling
items with the merchant. We also have the logic that the animal uses when it
comes to combat. Methods such as fortify, heal, attack, and retreat are here.

We also keep track of the pack that animal is a part of is in this class.

In this class we also assign the random names for each animal, from the
social security database that we scraped. We also equip items in this class
and keep track of which items are equipped.

All animals will belong to a pack. For more info on Packs please see
squirrelSimulator/animals/pack.py.
"""

import random, re
from inventory import Inventory
from items.item import Item
from minigame.combat.utils import *
from minigame.combat.utils.combatfunctions import attackComputation
from managers.nameManager import NAMES

class Animal():

    def __init__(self, name="", health=100, stamina = 100,xp=0, speed=1,
                 endurance=1,strength=1, intelligence=1, equipment=[],
                 inventorySize=9, inHand=None, armor=None, buffs=[]):
        """
        Here pass the traits that make up animal, we set a default value to
        give to those who implement subclasses an idea about how the data types
        that would be the best for the trait.

        Note: Health, Stamina are capped at 100. Inventory size is capped at 9
        for animals. 
        """
        #Give the animal a random name if none was provided
        if name == "":
            name = NAMES.getRandomName("standard")
        self._name = name

        #Set default species as the empty string
        self._species = ""

        #Basic Stats
        self._baseHealth = health
        self._health = health
        self._xp = xp
        self._baseStamina = stamina
        self._stamina = stamina

        self._baseHunger = 10
        self._hunger = self._baseHunger

        #Movement Stats
        self._speed = speed
        self._endurance = endurance

        #Combat Stats
        self._strength = strength
        self._attackModifers = 1
        self._defenseModifers = 1

        #Other Stats
        self._intelligence = intelligence
        self._acorns = 256

        #Equipment Carried by Animal
        self._inventory = Inventory(inventorySize)
        self._inventory.addItems(equipment)
        self._inhand = inHand
        self._armor = armor

        #Buffs currently on the animal
        self._buffs = buffs

        self._pack = None
        
        # string representation of what the animal did in combat
        self._combatStatus = ""

        # Variable holding the target of an attack if there was one
        self._combatTarget = None

    def getPack(self):
        """
        Here we return the Pack object that the animal belongs too.
        """
        return self._pack

    def setPack(self, pack):
        """
        Here we set the pack that the animal belongs too. This method
        is useful for the creation of a new animal and the transferring
        of one pack to another. 
        """
        self._pack = pack

    def getName(self):
        """Returns the name of the animal."""
        return self._name

    def rename(self, name):
        """Resets the name of the animal."""
        self._name = name

    def getCombatStatus(self):
        """
        Combat status is a variable that is a string representation
        of what the animal did during combat. It will write in simple
        english how the animal acted, ie. healed, fortified, attacked another
        animal (along with the damage dealt) or if the animal successfully
        killed another enemy. This will normally be an string type. 
        """
        return self._combatStatus

    def getCombatTarget(self):
        return self._target # Refactor this and the combat logic...

    def healLogic(self,opponents):
        """
        Given a list of opponents this method returns a boolean
        on whehter or not the animal believes that it is in its best
        move to heal for the turn. It calculates whether or not it can
        kill an opponent or do significant damage to the animal.

        Also if it has a low health and believes it will die, it will
        use a healing potion. We also check for a healing potion.
        """
        # opponents is a list
        damage = [(x,attackComputation(self,x),x.getHealth())
                  for x in opponents if x!=None]
        # calculates damage done and health an animal has
        attacks = [x for x in damage if x[1] >= x[2]]
        # checks to see if the animal can kill an opponent
        if self._health <= 20 and len(attacks) == 0:
            for x in self._inventory:
                if x.getAttribute("type") == "potions" and self._health <= 20:
                    self._combatStatus = self.getName() + " healed with a potion!"
                    self._target = self
                    return True
                    
            return False
        else:
            return False
        
    def fortifyLogic(self,opponents):
        """
        Given a list of opponents this method reuturns a boolean on whether
        or not the animal 
        """
        if self.getHealth() >= 20 and self.getHealth() <= 75:
            damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents if x!=None]
            #calculates the amount of damage that can be done vs the health
            attacks = [x for x in damage if x[1] <= 5]
            # runs a list comp that calculates if there are any animals that
            # the current animal will do less than 5 damamge against. 
            if len(attacks) == len(opponents):
                # checks to see if it can't do more than 5 damage to an animal
                self._combatStatus = self.getName() + " has fortified!"
                self._target = None
                return True
            elif 6 < random.randint(0,9): # 33% random change of fortifying 
                self._combatStatus = self.getName() + " has fortified!"
                self._target = None
                return True
            else:
                return False
        else:
            return False

    def damageOnOpponents(self,opponents):
        """
        This method calculates the damage that an animal will do to a
        list of opponents.
        """
        return [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents if x!=None]

    def kills(self,opponents):
        """
        Taking a list of opponents this method can caluculate the amount of
        damage that an animal can do to their opponenets.
        """
        return [x for x in self.damageOnOpponents(opponents) if x[1] >= x[2]]

    def attackLogic(self,opponents):
        """
        This method determines the logic calculations for attacking
        for an animal when they are fighing. It returns an animal.

        It first looks whether it can kill another animal, if so it returns
        the animal. Then it looks for the highest damaage animal
        and returns that hype. 
        """
        damage = self.damageOnOpponents(opponents)
        kills = self.kills(opponents) # calculates the kills
        random.shuffle(kills) # shuffles the kill so it's not always the player
        if len(kills) > 0:
            a = kills[0][0]
            self._combatStatus = self.getName() + " has killed " + a.getName()
            self._target = a
            return kills[0][0]
        else:
            damage.sort(key = lambda x: x[1])
            # sorts the damage from lowest to highest
            self._combatStatus = self.getName() + " did " + str(damage[-1][1])+ " damage to " + \
                                 (damage[-1][0]).getName()
            self._target = damage[-1][0]
            return damage[-1][0] #returns the highest damage animal
        
    # Basic Stats
    def getHealth(self):
        """Returns the health of the animal."""
        return self._health

    def getBaseHealth(self):
        """Returns the base health of the animal. The default is 100."""
        return self._baseHealth

    def increaseBaseHealth(self, increase):
        """Increases the animal's base health."""
        self._baseHealth += increase

    def decreaseBaseHealth(self, decrease):
        """Decreases the animal's base health."""
        self._baseHealth -= decrease

    def setHealth(self, health):
        """Sets the health of the animal equal to a value."""
        self._health = health

    def heal(self, health):
        """
        Increments the health counter.

        Parameters
        ----------
        -> int: health
            The amount of health to increment character health by

        Will increment the health of the animal up to its maximum health by
        inputted health amount. 
        """
        while self._health < self._baseHealth and health > 0:
            self._health += 1
            health -= 1

    def loseHealth(self, health):
        """
        Decrements the health counter.

        Parameters
        ----------
        -> int: health
            The amount of health to increment character health by

        Will decrease the health of the animal up to its maximum health by
        inputted health amount.
        """
        self._health = max(0, self._health-health)

    def isDead(self):
        """
        Returns boolean if the animal has less than 0 health. Will be False
        if less than 0.
        """
        return self._health <= 0
    
    def getBaseStamina(self):
        """Returns the base stamina of the animal."""
        return self._baseStamina

    def setBaseStamina(self,newBaseStamina):
        """Returns the base stamina of the animal."""
        self._baseStamina = newBaseStamina

    def getStamina(self):
        """Returns the stamina of the animal."""
        return self._stamina

    def setStamina(self,stamina):
        """Can update the stamina."""
        self._stamina = stamina

    def getStaminaCost(self):
        """
        Outputs an interval of possible stamina usage.
        Checks if there is a tool in hand. If no tool, then no stamina used.

        The method will generate an interval of plus/minus 10% to the current
        stamina.

        Will return a tuple of the stamina interval. 
        """
        if self.hasToolInHand():
            return self._inhand.getStaminaCost() # Need to add getStamina()
        else:
            return 0

    def loseStamina(self,stamina):
        """
        Uses the stamina to lose the stamina. 
        """
        if self._stamina - stamina < 0:
            self._stamina = 0
        else:
            self._stamina -= stamina

    def getXP(self):
        """Returns the XP of the player."""
        return self._xp

    def setXP(self, xp):
        """Sets the XP of the player to a value."""
        self._xp = xp

    def incrementXP(self, xp):
        """Increments the for the animal."""
        self._xp += xp

    def getHunger(self):
        """Returns the hunger level of the animal."""
        return self._hunger

    def setHunger(self, hunger):
        """Sets the hunger level of the animal."""
        self._hunger = hunger

    def getBaseHunger(self):
        """
        Returns the base hunger of an animal. The default is 10 for
        all animals.
        """
        return self._baseHunger

    def decrementHunger(self,amount=1):
        """
        Decrements an animals hunger, the default is one.
        """
        self._hunger = max(0, self._hunger-amount)

    def increaseHunger(self, amount=1):
        """
        Increases the hunger of the animal.
        """
        self._hunger = min(self._hunger+amount, self._baseHunger)

    def isStarving(self):
        """
        Returns a boolean of the animal has a hunger of 0.
        """
        return self._hunger == 0

    def getSpeed(self):
        """
        Returns the speed of the animal.
        """
        return self._speed

    def setSpeed(self, speed):
        """
        Sets the speed of the animal.
        """
        self._speed = speed

    def incrementSpeed(self, speed):
        """
        Increments the speed.
        """
        self._speed += speed

    def getEndurance(self):
        """
        Returns the endurance of the animal.
        """
        return self._endurance

    def setEndurance(self, endurance):
        """
        Sets the endurance of the animal. 
        """
        self._endurance = endurance

    def getAcorns(self):
        """
        Returns the acorns of the animal. 
        """
        return self._acorns

    def setAcorns(self,acorns):
        """
        Sets the acorns of the animal.
        """
        self._acorns = acorns

    def buyLogic(self,item,cost):
        """Returns boolean if animal wants to buy item."""
        if self._acorns >= item.getAttribute("value") and item.isBuyable():
            return True
        else:
            return False

    def buyItem(self,item,cost):
        """
        Buys an item from the merchant and adds it to the players's
        inventory.

        Parameters
        ----------
        item: an Item object
        cost: an integer representing the cost
        """
        assert type(item) == Item
        assert type(cost) == int
        self._inventory.addItem(item)
        self._acorns = self._acorns - cost

    def sellLogic(self,item,price):
        """Returns boolean if animal wants to sell item."""
        if item in self._inventory and item.isSellable():
            return True
        else:
            return False

    def sellItem(self,item,price):
        """
        Sells an item to the merchant and removes it to the players's
        inventory.

        Parameters
        ----------
        item: an Item object
        cost: an integer representing the cost
        """
        assert type(item) == Item
        assert type(price) == int
        self._inventory.removeItem(item)
        self._acorns = self._acorns + price

    def getStrength(self):
        """
        Returns the strength of the animal.
        """
        return self._strength

    def setStrength(self, strength):
        """
        Sets the strength of the animal.
        """
        self._strength = strength

    def getIntelligence(self):
        """
        Returns the intelligence of the animal.
        """
        return self._intelligence

    def setIntelligence(self, intel):
        """
        Sets the intelligence of the animal.
        """
        self._intelligence = intel

    def incrementEndurance(self, endurance):
        """
        Sets the endurance of the of the animal.
        """
        self._endurance += endurance
        
    # modifers 

    def getAttackModifers(self):
        """
        Returns the attack modifers.
        """
        return self._attackModifers

    def addAttackModifers(self,modifer):
        """
        Adds to the attack modifers.
        """
        self._attackModifers += modifer

    def resetAttackModifers(self):
        """
        Resets the attack modifers.
        """
        self._attackModifers = 1

    def getDefenseModifers(self):
        """
        Returns the defense modifers.
        """
        return self._defenseModifers

    def addDefenseModifers(self,modifer):
        """
        Adds to the defense modifers.
        """
        self._defenseModifers += modifer

    def resetDefenseModifers(self):
        """
        Resets the defense modifers.
        """
        self._defenseModifers = 1

    def getInventory(self):
        """
        Returns the inventory of the animal.
        """
        return self._inventory

    def setInventory(self, inv):
        """
        Sets the inventory of the animal. Must be an inventory object.
        """
        self._inventory = inv

    def equipItem(self, item):
        """
        This allows the player to equip the item. Must be a weapon item type.
        """
        self._inhand = item

    def unEquipItem(self):
        """
        Allows the player unequip an item they are holding.
        """
        self._inventory.addItem(self._inhand)
        self._inhand = None

    def unEquipArmor(self):
        """
        Allows the player unequip armor they are holding.
        """      
        self._inventory.addItem(self._armor)
        self._armor = None
        
    def equipArmor(self, armor):
        """
        This allows player to put on armor. Must pass an armor item type.
        """
        self._armor = armor

    def getArmor(self):
        """
        Returns the armor the player has.
        """
        return self._armor

    def isEquipped(self):
        """
        Checks if animal has an item equipped. Returns a boolean.
        """
        return self._inhand != None

    def getEquipItem(self):
        """
        Returns the item in the animal's hand.
        """
        return self._inhand

    def hasArmor(self):
        """
        Returns a boolean if the animal has armor. 
        """
        return self._armor != None

    def getEquipItemName(self):
        """
        Returns the name of the item that the player has equipped.
        """
        if self._inhand == None:
            return "" 
        else:
            return type(self._inhand).__name__

    def getArmorsName(self):
        """
        Returns the name of the armor that the player has equipped.
        """
        if self._armor == None:
            return ""
        else:
            return re.sub(r"(\w)([A-Z])", r"\1 \2", type(self._armor).__name__)

    def getStats(self):
        """Used by weapons and armors to check if they are usable by the entity"""
        return (self._xp, self._strength, self._intelligence, self._endurance)


    def shareItem(self,item):
        """
        The logic behind why an animal would share an item into
        their pack inventory
        """
        #if item.isSharable():
        return 0

    def takeItem(self,item):
        """
        The logic behind why an animal would take an item from
        their pack inventory
        """        
        return 0

    def __repr__(self):
        """
        Returns a string representation of the animal.
        """
        return "Name:          " + self._name + \
               "\nSpecies:       " + self._species + \
               "\nHealth:        " + str(self._health) + "/" + str(self._baseHealth) + \
               "\nStamina:       " + str(self._stamina) + "/" + str(self._baseStamina) + \
               "\nAcorns:        " + str(self._acorns) + \
               "\nXP:            " + str(self._xp) + \
               "\nSpeed:         " + str(self._speed) + \
               "\nEndurance:     " + str(self._endurance) + \
               "\nHolding:       " + self.getEquipItemName() + \
               "\nArmor:         " + self.getArmorsName() + \
               "\nInventory:     " + str(self._inventory) + \
               "\nBuffs:         " + str([type(x).__name__ for x in self._buffs])
               
