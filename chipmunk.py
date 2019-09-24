
from npc import NPC

AGGRESSION   = (0,2)
HEALTH       = (10,15)
SPEED        = (12,18)
ENDURANCE    = (6,10)
DAMAGE       = (4,6)
ATTACK_SPEED = (1,2)
DEFENSE      = (5,7)

class Chipmunk(NPC):

    def __init__(self, name):

        super().__init__(name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
