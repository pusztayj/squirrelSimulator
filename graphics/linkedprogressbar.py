
import pygame
from .progressbar import ProgressBar 

class LinkedProgressBar():

    def __init__(self, entity, position, length, maxStat, actStat, borderWidth=1,
                 borderColor=(0,0,0), backgroundColor=(120,120,120),
                 barColor=(255,0,0)):

        self._progressBar = ProgressBar(position, length, maxStat, actStat,
                                        borderWidth, borderColor, backgroundColor,
                                        barColor)
        self._entity = entity

    def update(self):
        self._progressBar.setProgress(self._entity.getHealth())

    def draw(self):
        self._progressBar.draw()
        
