
import pygame, random
from level import Level
from modules.drawable import Drawable
from modules.soundManager import SoundManager

class CombatLevel(Level):

    def __init__(self, player, SCREEN_SIZE):
        super().__init__()

        self._SCREEN_SIZE = (1200,500)

        self._songs = ["battle1.mp3","battle2.mp3"]
        self._currentSong = random.choice(self._songs)

        self._player = player

        self._background = Drawable("merchantForest2.png",
                                    (0,0), worldBound=False)

        SoundManager.getInstance().playMusic(self._currentSong)

    def draw(self, screen):

        self._background.draw(screen)

    def handleEvent(self, event):
        pass

    def update(self, ticks):
        pass
