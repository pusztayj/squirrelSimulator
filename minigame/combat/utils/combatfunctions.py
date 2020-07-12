
attackDamage = {(0.0,1):0,(0.25,1): 5, (0.5,1): 10, (0.75,1): 20, (1,1): 30,
                (1.25,1): 33, (1.5,1): 35, (1.75,1): 40, (2,1): 45, (2.25,1): 47,
                (2.5,1): 50, (2.75,1): 70, (3,1): 90}

def attack(attacker, defender):
    """
    Executes an attack where one creature gives damage to another one.
    Damage dealt is calculated on a ratio of strengths. It takes a ratio
    between attacker's strength and defenders strength.

    It awards damage based on the attack-damage dictionary.
    """
    
    damage = attackComputation(attacker,defender)
    defender.loseHealth(damage)
    # potential gain xp
    # potential stamina loss


def attackComputation(attacker,defender):
    """
    Calculates the damage dealt between an attacker and a defender.
    """
    attacker.resetDefenseModifers()
    if attacker.getEquipItem() != None:
        attack_strength = (attacker.getStrength() + \
                               (attacker.getEquipItem().getAttribute("strength"))) * \
                               attacker.getAttackModifers()
    else:
        attack_strength = attacker.getStrength()*attacker.getAttackModifers()

    if defender.getArmor() != None:
        defense_strength = (defender.getStrength() + \
                           (defender.getArmor().getAttribute("strength"))) * \
                           defender.getDefenseModifers()
    else:
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
        animal.heal(potion.getAttribute("healthBoost"))


def retreat(animal):
    """
    Forces an animal to retreat
    """
    animal.resetDefenseModifers()
