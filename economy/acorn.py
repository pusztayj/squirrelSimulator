
from modules.drawable import Drawable

class Acorn(Drawable):

    def __init__(self, pos, worldBound=True):
        super().__init__("acorn.png", pos, worldBound=worldBound)
        self._collected = False

    def collected(self):
        self._collected = True

    def isCollected(self):
        return self._collected
