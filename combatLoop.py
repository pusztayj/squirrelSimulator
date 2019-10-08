
from animals.animal import Animal
from animals.chipmunk import Chipmunk
from animals.fox import Fox
from animals.bear import Bear
from animals.deer import Deer
import items.item, random, buffs.buff, animals.pack
from utils import *

def fight(entityOne, entityTwo):
    assert issubclass(type(entityOne), Animal)
    assert issubclass(type(entityTwo), Animal)
    retreat = False
    while not retreat:

        # First entity attack phase
        combatPhase(entityOne, entityTwo)
        if entityTwo.isDead():
            print(entityTwo.getName(), "has died.")
            break
        # Second entity attack phase
        combatPhase(entityTwo, entityOne)
        if entityOne.isDead():
            print(entityOne.getName(), "has died.")
            break

def combatPhase(entityOne, entityTwo):
    attackStat = entityOne.dealDamage()
    defenseStat = entityTwo.defend()
    damageDealt = attackStat - defenseStat
    if damageDealt < 0: damageDealt = 0
    if entityOne.hasToolInHand():
        wear = random.randint(0,4)
        if wear == 0:
            entityOne.getToolInHand().decrementDurability()     
    print(entityOne.getName(), "deals", damageDealt, "to", entityTwo.getName())
    entityTwo.loseHealth(damageDealt)
        
