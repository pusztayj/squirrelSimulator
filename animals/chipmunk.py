
from .npc import NPC

AGGRESSION   = (0,2)
SPEED        = (12,18)
ENDURANCE    = (6,10)
STRENGTH     = 8 

class Chipmunk(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "tempChipmunk.png", pos,
                     AGGRESSION, SPEED, ENDURANCE,STRENGTH)
