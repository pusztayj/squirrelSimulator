import math
import random

def retreatLostAcorns(animal):
    """
    Acorns lost for retreating from a battle
    """
    return math.ceil(animal.getAcorns()*random.uniform(0,0.5)) # add to spreadsheet
     
def retreatItemLost(animal):
    """
    Chance of item lost from retreating from battle.
    """
    if 10 <= random.randint(0,100) and len(animal.getInventory()) != 0:
        item = random.choice(animal.getInventory())
        return item
    else:
        return None
