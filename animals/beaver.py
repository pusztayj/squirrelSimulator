from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 20

class Beaver(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "beaver.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)

