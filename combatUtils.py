"""
In this file we create the functions for the combat game.
"""

from items.items import *

attackDamage = {(0.25,1): 5, (0.5,1): 10, (0.75,1): 20, (1,1): 30,
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
                         
    ratio = round((attack_strength/defense_strength) * 4) / 4  
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

def combat(playerTeam,enemyTeam):
    # teams needs to be pack objects
    playerTeam = playerTeam.getMembers()
    enemyTeam = enemyTeam.getMembers()
    participants = list()
    for x in range(3): # creates an alteration of the lists so the combat loop
        # can work
        participants += playerTeam[x:x+1]
        participants += enemyTeam[x:x+1]
    for animal in participants:
        if type(animal) == type(Player()):
            pass
        else:
            if animal in playerTeam:
                move(animal,enemyTeam)
            else:
                move(animal,playerTeam)
