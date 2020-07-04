from economy.merchant import Merchant
from animals import Creature, Pack


        
def giveAcorns(entity, amount):
   """Gives an entity a given number of acorns"""
   entity.setAcorns(entity.getAcorns() + amount)

def giveXP(entity, amount):
   """Gives an entity a given number of XP"""
   entity.setXP(entity.getXP() + amount)

def spawnMerchant(mainGame, position):
   """Spawns a merchant at a given position"""
   mainGame._merchants.append(Merchant(pos=position))

def fastForward(mainGame, amount):
   """Fastforwards the game clock by a given amount"""
   hourLen = mainGame._worldClock.getHourLength()
   time, mode = amount
   if mode == "hours":
      mainGame._worldClock._time += (time*hourLen)
   if mode == "days":
      mainGame._worldClock._time += (time*hourLen*24)

def setHealth(entity, amount):
   """Sets an entity's health to a given amount"""
   amount = max(0,min(amount,entity.getBaseHealth()))
   entity.setHealth(amount)

def spawnAnimal(mainGame, species, position, friendScore):
   """Spawns an animal given a type, position, and friendScore"""
   animal = Creature(species.lower(), pos=position)
   animal.setFriendScore(friendScore)
   p = Pack(animal)
   animal.setPack(p)
   mainGame._packs.append(p)

# Dictionary of cheat codes
codes = {1:giveAcorns,2:giveXP,3:spawnMerchant,
               4:fastForward,5:setHealth,6:spawnAnimal}

# Group codes into types by their inputs
types = {1:(1,2,4), 2:(3,4), 3:(6,)}
