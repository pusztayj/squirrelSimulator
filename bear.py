
from npc import NPC

AGGRESSION   = (8,10)
HEALTH       = (50,75)
SPEED        = (15,20)
ENDURANCE    = (8,10)
DAMAGE       = (20,24)
ATTACK_SPEED = (6,8)
DEFENSE      = (10,12)

class Bear(NPC):

    def __init__(self, name=""):

        super().__init__(name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
