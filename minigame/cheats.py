from minigame.merchant.utils import *
from animals import Creature, Pack
from items.item import Item
from polybius.managers import CONSTANTS

def giveAcorns(entity, amount):
   """Gives an entity a given number of acorns"""
   entity.setAcorns(entity.getAcorns() + amount)

def giveXP(entity, amount):
   """Gives an entity a given number of XP"""
   entity.setXP(entity.getXP() + amount)

def spawnMerchant(mainGame, position):
   """Spawns a merchant at a given position"""
   mainGame._merchants.append(Merchant(pos=position))

def fastForward(amount):
   """Fastforwards the game clock by a given amount"""
   clock = CONSTANTS.get("worldClock")
   hourLen = clock.getHourLength()
   time, mode = amount
   if mode == "hours":
      clock._time += (time*hourLen)
   if mode == "days":
      clock._time += (time*hourLen*24)

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

def giveItem(entity, i, quant=1):
   """Gives an entity an item"""
   for x in range(quant):
      item = Item(i, CONSTANTS.get("player"))
      entity.getInventory().addItem(item)

# Dictionary of cheat codes
codes = {1:giveAcorns,2:giveXP,3:spawnMerchant,
         4:fastForward,5:setHealth,6:spawnAnimal,
         7:giveItem}

# Group codes into types by their inputs
types = {1:(1,2,5,7), 2:(3,), 3:(6,), 4:(7,), 5:(4,)}
