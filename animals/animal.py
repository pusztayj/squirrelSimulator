"""
@authors: Justn Pusztay, Trevor Stalnaker

The animal class.
"""

import random, shelve
from inventory import Inventory
from items.item import Item
from minigame.combatUtils import *

class Animal():

    def __init__(self, name="", health=100, stamina = 100,xp=0, speed=1, endurance=1,
                 combatDamage=10, strength=1,
                 intelligence=1, equipment=[], inventorySize=9,
                 inHand=None, armor=None, buffs=[]):

        #Give the animal a random name if none was provided
        if name == "":
            shelf = shelve.open("data")
            name = random.choice(shelf["names"])
            shelf.close()
        self._name = name

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

        self._combatStatus = ""

    def getPack(self):
        return self._pack

    def setPack(self, pack):
        self._pack = pack

    def getName(self):
        """Returns the name of the animal."""
        return self._name

    def rename(self, name):
        """Resets the name of the animal."""
        self._name = name

    def getCombatStatus(self):
        return self._combatStatus

    def healLogic(self,opponents):
        # opponents is a list
        damage = [(x,attackComputation(self,x),x.getHealth())
                  for x in opponents if x!=None]
        # calculates damage done and health an animal has
        attacks = [x for x in damage if x[1] >= x[2]]
        # checks to see if the animal can kill an opponent
        if self._health <= 20 and len(attacks) == 0:
            for x in self._inventory:
                if type(x) == type(Potions()) and self._health <= 20:
                    self._combatStatus = self.getName() + "healed with a potion!"
                    return True
                    
            return False
        else:
            return False
        
    def fortifyLogic(self,opponents):
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
                return True
            elif 6 < random.randint(0,9): # 33% random change of fortifying 
                self._combatStatus = self.getName() + " has fortified!"
                return True
            else:
                return False
        else:
            return False

    def damageOnOpponents(self,opponents):
        return [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents if x!=None]

    def kills(self,opponents):
        return [x for x in self.damageOnOpponents(opponents) if x[1] >= x[2]]

    def attackLogic(self,opponents):
        damage = self.damageOnOpponents(opponents)
        kills = self.kills(opponents) # calculates the kills
        random.shuffle(kills) # shuffles the kill so it's not always the player
        if len(kills) > 0:
            a = kills[0][0]
            self._combatStatus = self.getName() + " has killed " + a.getName()
            return kills[0][0]
        else:
            damage.sort(key = lambda x: x[1]) #could shuffle to make more stupid
            # sorts the damage from lowest to highest
            self._combatStatus = self.getName() + " did " + str(damage[-1][1])+ " damage to " + \
                                 (damage[-1][0]).getName()
            return damage[-1][0] #returns the highest damage animal
        
    # Basic Stats
    def getHealth(self):
        return self._health

    def getBaseHealth(self):
        return self._baseHealth

    def increaseBaseHealth(self, increase):
        self._baseHealth += increase

    def decreaseBaseHealth(self, decrease):
        self._baseHealth -= decrease

    def setHealth(self, health):
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
        return self._xp

    def setXP(self, xp):
        self._xp = xp

    def incrementXP(self, xp):
        self._xp += xp

    def getHunger(self):
        return self._hunger

    def setHunger(self, hunger):
        self._hunger = hunger

    def getBaseHunger(self):
        return self._baseHunger

    def decrementHunger(self,amount=1):
        self._hunger = max(0, self._hunger-amount)

    def increaseHunger(self, amount=1):
        self._hunger = min(self._hunger+amount, self._baseHunger)

    def isStarving(self):
        return self._hunger == 0

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def incrementSpeed(self, speed):
        self._speed += speed

    def getEndurance(self):
        return self._endurance

    def setEndurance(self, endurance):
        self._endurance = endurance

    def getAcorns(self):
        return self._acorns

    def setAcorns(self,acorns):
        self._acorns = acorns

    def buyLogic(self,item,cost):
        """Returns boolean if animal wants to buy item."""
        if self._acorns >= item.getValue() and item.isBuyable():
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
        assert issubclass(type(item),Item)
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
        assert issubclass(type(item),Item)
        assert type(price) == int
        self._inventory.removeItem(item)
        self._acorns = self._acorns + price

    def getStrength(self):
        return self._strength

    def setStrength(self, strength):
        self._strength = strength

    def getIntelligence(self):
        return self._intelligence

    def setIntelligence(self, intel):
        self._intelligence = intel

    def incrementEndurance(self, endurance):
        self._endurance += endurance
        
    # modifers 

    def getAttackModifers(self):
        return self._attackModifers

    def addAttackModifers(self,modifer):
        self._attackModifers += modifer

    def resetAttackModifers(self):
        self._attackModifers = 1

    def getDefenseModifers(self):
        return self._defenseModifers

    def addDefenseModifers(self,modifer):
        self._defenseModifers += modifer

    def resetDefenseModifers(self):
        self._defenseModifers = 1

    def combatMoveLogic(self,target):
        if self._health <= 25 and (Potions() in self._inventory):
            return "heal"

    def getInventory(self):
        return self._inventory

    def setInventory(self, inv):
        self._inventory = inv

    def equipItem(self, item):
        self._inhand = item

    def unEquipItem(self):
        self._inventory.addItem(self._inhand)
        self._inhand = None

    def unEquipArmor(self):
        self._inventory.addItem(self._armor)
        self._armor = None
        
    def equipArmor(self, armor):
        self._armor = armor

    def getArmor(self):
        return self._armor

    def isEquipped(self):
        return self._inhand != None

    def getEquipItem(self):
        return self._inhand

    def hasArmor(self):
        return self._armor != None

    def getEquipItemName(self):
        if self._inhand == None:
            return "" # Empty string might be better
        else:
            return type(self._inhand).__name__

    def getArmorsName(self):
        if self._armor == None:
            return ""
        else:
            return type(self._armor).__name__

    def getStats(self):
        """Used by weapons and armors to check if they are usable by the entity"""
        return (self._xp, self._strength, self._intelligence, self._endurance)

    def giveBuff(self, buff):
        self._buffs.append(buff)

    def removeBuff(self, buff):
        self._buffs.remove(buff)

    def applyAndUpdateBuffs(self):
        self._buffs = [buff for buff in self._buffs if not buff.expired()]
        for buff in self._buffs:
            buff.applyBuff()

    def __repr__(self):
        return "Name:          " + self._name + \
               "\nSpecies:       " + str(type(self).__name__) + \
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
               
