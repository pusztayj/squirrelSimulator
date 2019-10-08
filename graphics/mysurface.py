
from drawable import Drawable

class MySurface(Drawable):

    def __init__(self, surface, position=(0,0)):
        super().__init__("", position, worldBound=False)
        self._image = surface
