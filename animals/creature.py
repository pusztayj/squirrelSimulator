
from .animalManager import ANIMALS
from .npc import NPC
from modules.animated import Animated
import csv
import pprint

class Creature(NPC):

    def __init__(self, species, name="", pos=(0,0), worldBound=True):
        """
        We set the appropriate stats to create the NPC for the deer.
        We also specify the rows that we need for the animations.
        """
        stats = ANIMALS.getStats(species)
          
        NPC.__init__(self, name, stats["image"], pos,
                     stats["aggression"], stats["speed"],
                     stats["endurance"], stats["strength"])

        self.setWorldBound(worldBound)

        self._species = species
        self._maxVelocity = stats["maxVelocity"]

        # Specify which rows contain which animations
        self._standRow = stats["standRow"]
        self._walkRow = stats["walkRow"]
        self._forwardRow = stats["forwardRow"]
        self._backwardRow = stats["backwardRow"]
        
        # Specify how many frames for each animation
        self._standFrames    = stats["standFrames"]
        self._walkFrames     = stats["walkFrames"]
        self._forwardFrames  = stats["forwardFrames"]
        self._backwardFrames = stats["backwardFrames"]


    
