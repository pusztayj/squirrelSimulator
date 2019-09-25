
from npc import NPC

AGGRESSION   = (0,5)
HEALTH       = (25,30)
SPEED        = (15,20)
ENDURANCE    = (8,10)
DAMAGE       = (12,15)
ATTACK_SPEED = (3,4)
DEFENSE      = (6,8)

class Fox(NPC):

    def __init__(self, name=""):

        super().__init__(name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
