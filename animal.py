"""
@authors: Justn Pusztay, Trevor Stalnaker

The animal class.
"""

import random, shelve
from inventory import Inventory

class Animal():

    def __init__(self, name="", health=100, stamina = 100,xp=0, speed=1, endurance=1,
                 combatDamage=10, attackSpeed=1, defensiveStat=10, strength=1,
                 intelligence=1, equipment=[], inventorySize=10,
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

        #Movement Stats
        self._speed = speed
        self._endurance = endurance

        #Combat Stats
        self._baseDamage = combatDamage
        self._attackSpeed = attackSpeed
        self._defensiveStat = defensiveStat

        #Other Stats
        self._strength = strength
        self._intelligence = intelligence
        self._money = 0

        #Equipment Carried by Animal
        self._inventory = Inventory(inventorySize)
        self._inventory.addItems(equipment)
        self._inhand = inHand
        self._armor = armor

        #Buffs currently on the animal
        self._buffs = buffs

    def getName(self):
        """Returns the name of the animal."""
        return self._name

    def rename(self, name):
        """Resets the name of the animal."""
        self._name = name
        
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
        self._health -= health

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

    def getMoney(self):
        return self._money

    def setMoney(self,money):
        self._money = money

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
        if self._money >= cost and item.isBuyable():
            self._inventory.addItem(item)
            self._money = self._money - cost

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
        if item in self._inventory and item.isSellable():
            self._inventory.removeItem(item)
            self._money = self._money + price

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

    def getBaseDamage(self):
        return self._baseDamage

    def setBaseDamage(self, damage):
        self._baseDamage = damage

    def incrementBaseDamage(self, damage):
        self._baseDamage += damage

    def getCurrentDamageRange(self):
        """
        Outputs an interval of possible damage. Checks if there is a tool in
        hand. If no tool, then animal punches.

        The method will generate an interval of plus/minus 10% to the current
        damage.

        Will return a tuple of the damage interval. 
        """
        if self.hasToolInHand():
            damage = self._inhand.getDamage()
        else:
            damage = self._baseDamage
        margin = round(damage * .1) 
        return (damage-margin, damage+margin)

    def dealDamage(self):
        """
        Outputs an integer with the damage that will be dealt by the weapon.

        Takes an adjusted damage from the damageRange and then multiples it
        by a fraction in the range of 1/4 to 3/4. That will be the damage
        returned.
        """
        damageRange = self.getCurrentDamageRange()
        adjustedDamage = random.randint(damageRange[0],damageRange[1])
        adjustedDamage += (((adjustedDamage * 0.01) * self._baseDamage) * \
                           random.randint(0,1))
        return max(0, round(adjustedDamage))

    def getAttackSpeed(self):
        return self._attackSpeed

    def setAttackSpeed(self, speed):
        self._attackSpeed = speed

    def incrementAttackSpeed(self, speed):
        self._attackSpeed += speed

    def getDefensiveStat(self):
        return self._defensiveStat

    def setDefensiveStat(self, defense):
        self._defensiveStat = defense

    def getCurrentProtectionRange(self):
        """
        Outputs an interval of possible damage absorption based on armor.
        Checks if animal has armor.

        The method will generate an interval of plus/minus 10% to the current
        damage.

        Will return a tuple of the damage interval. 
        """
        if self.hasArmor():
            protect = self._armor.getProtection()
        else:
            protect = self._defensiveStat
        margin = round(protect * .1) 
        return (protect-margin, protect+margin)

    def defend(self):
        """
        Outputs an intenger for the amount of protection an animal has.

        Takes an adjusted defend from the defend and then multiples it
        by a fraction in the range of 1/4 to 3/4. That will be the defend
        number returned.
        """
        defendRange = self.getCurrentProtectionRange()
        adjustedProtect = random.randint(defendRange[0],defendRange[1])
        adjustedProtect += (((adjustedProtect * 0.01) * self._defensiveStat) * \
                           random.randint(0,1))
        return max(0,round(adjustedProtect))        

    def getInventory(self):
        return self._inventory

    def equipTool(self, tool):
        self._inhand = tool

    def unEquipTool(self):
        self._inventory.addItem(self._inhand)
        self._inhand = None

    def unEquipArmor(self):
        self._inventory.addItem(self._armor)
        self._armor = None
        
    def equipArmor(self, armor):
        self._armor = armor

    def hasToolInHand(self):
        return self._inhand != None

    def getToolInHand(self):
        return self._inhand

    def hasArmor(self):
        return self._armor != None

    def getToolInHandsName(self):
        if self._inhand == None:
            return "Nothing" # Empty string might be better
        else:
            return type(self._inhand).__name__

    def getArmorsName(self):
        if self._armor == None:
            return "Nothing"
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
        damageRange = self.getCurrentDamageRange()
        protectRange = self.getCurrentProtectionRange()
        if damageRange[0] == damageRange[1]:
            drange = str(damageRange[0])
        else:
            drange = str(damageRange[0]) + "-" + str(damageRange[1])
        if protectRange[0] == protectRange[1]:
            prange = str(protectRange[0])
        else:
            prange = str(protectRange[0]) + "-" + str(protectRange[1])

        
            
        return "Name:          " + self._name + \
               "\nSpecies:       " + str(type(self).__name__) + \
               "\nHealth:        " + str(self._health) + "/" + str(self._baseHealth) + \
               "\nStamina:       " + str(self._stamina) + "/" + str(self._baseStamina) + \
               "\nXP:            " + str(self._xp) + \
               "\nSpeed:         " + str(self._speed) + \
               "\nEndurance:     " + str(self._endurance) + \
               "\nCombat Damage: " + drange + \
               "\nAttack Speed:  " + str(self._attackSpeed) + \
               "\nDefense:       " + prange + \
               "\nHolding:       " + self.getToolInHandsName() + \
               "\nArmor:         " + self.getArmorsName() + \
               "\nInventory:     " + str(self._inventory) + \
               "\nBuffs:         " + str([type(x).__name__ for x in self._buffs])
               
