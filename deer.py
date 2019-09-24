
from npc import NPC

AGGRESSION   = (0,1)
HEALTH       = (14,18)
SPEED        = (18,24)
ENDURANCE    = (6,10)
DAMAGE       = (6,8)
ATTACK_SPEED = (1,2)
DEFENSE      = (3,5)

class Deer(NPC):

    def __init__(self, name):

        super().__init__(name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
