"""
In this file we create the functions for the combat game.
"""


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
    
    attacker.resetDefenseModifers()

    i = 0; j = 0
    if attacker.isEquipped(): i = 1
    if defender.hasArmor(): j = 1

    attack_strength = (attacker.getStrength() + \
                       (i*attacker.getEquipItem().getStrength())) * \
                       attacker.getAttackModifers()

    defense_strength = (defender.getStrength() + \
                       (j*defender.getArmor().getStrength())) * \
                       defender.getDefenseModifers()

    ratio = round((attack_strength/defense_strength) * 4) / 4  
    damage = attackDamage[(ratio,1)]
    defender.loseHealth(damage)
    # potential gain xp
    # potential stamina loss

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
        