
from animal import Animal
import random

class NPC(Animal):


    def __init__(self, name, agression, health, speed, endurance, damage,
                 attack_speed, defense):
        
        super().__init__(name=name,
                         health=random.randint(health[0],health[1]),
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         combatDamage=random.randint(damage[0],damage[1]),
                         attackSpeed=random.randint(attack_speed[0],attack_speed[1]),
                         defensiveStat=random.randint(defense[0],defense[1]))
        
        self._aggressionLevel = agression
            

