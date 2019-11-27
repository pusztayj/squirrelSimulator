"""
Author: Trevor Stalnaker
File: happinessface.py
"""

from modules.drawable import Drawable
from modules.frameManager import FRAMES
import pygame

class HappinessFace(Drawable):

    def __init__(self, pos):

        Drawable.__init__(self, "face_0.png", pos, worldBound=False)

    def setFace(self, happyStat):
        if 0 <= happyStat < 20:
            self._image = FRAMES.getFrame("face_4.png")
        elif 20 <= happyStat < 40:
            self._image = FRAMES.getFrame("face_3.png")
        elif 40 <= happyStat < 60:
            self._image = FRAMES.getFrame("face_2.png")
        elif 60 <= happyStat < 80:
            self._image = FRAMES.getFrame("face_1.png")
        else:
            self._image = FRAMES.getFrame("face_0.png")
