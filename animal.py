
import random

class Animal():

    def __init__(self, name="", health=100, xp=0, speed=1, endurance=1, combatDamage=10,
                 attackSpeed=1, defensiveStat=10, strength=1, intelligence=1,
                 equipment=[], inventorySize=10,
                 inHand=None, armor=None, buffs=[]):

        self._name = name

        #Basic Stats
        self._baseHealth = health
        self._health = health
        self._xp = xp

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

        #Equipment Carried by Animal
        self._equipment = equipment
        self._inventory_size = inventorySize
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
        if adjustedDamage < 0: # Damage cannot be negative
            return 0
        else:
            return round(adjustedDamage* (random.randint(25,75)/100))

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
        if adjustedProtect < 0: # Damage cannot be negative
            return 0
        else:
            return round(adjustedProtect* (random.randint(25,75)/100))        

    def getEquipment(self):
        return self._equipment

    def hasItem(self, item):
        return item in self._equipment

    def addItem(self, item):
        self._equipment.append(item)

    def removeItem(self, item):
        self._equipment.remove(item)

    def getItems(self):
        return self._equipment

    def getInventorySpace(self):
        return self._inventory_space

    def equipTool(self, tool):
        self._inhand = tool

    def unEquipTool(self):
        self._equipment.append(self._inhand)
        self._inhand = None
        
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
            return "Nothing"
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
               "\nXP:            " + str(self._xp) + \
               "\nSpeed:         " + str(self._speed) + \
               "\nEndurance:     " + str(self._endurance) + \
               "\nCombat Damage: " + drange + \
               "\nAttack Speed:  " + str(self._attackSpeed) + \
               "\nDefense:       " + prange + \
               "\nHolding:       " + self.getToolInHandsName() + \
               "\nArmor:         " + self.getArmorsName() + \
               "\nInventory:     " + str(self._equipment) + \
               "\nBuffs:         " + str([type(x).__name__ for x in self._buffs])
               
