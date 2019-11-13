import pygame
from modules.drawable import Drawable

class ItemBlock(Drawable):

    def __init__(self, pos, dimensions=(77,50), item=None, selected=False):
        super().__init__("", pos, worldBound = False)
        self._item = item
        self._width = dimensions[0]
        self._height = dimensions[1]

        self._borderColor = (0,0,0)
        self._selectedBorder = (150,150,150)
        self._backgroundColor = (100,100,100)
        self._borderWidth = 1

        self._transparency = 200

        self._selected = selected

        self.updateBlock()

    def setItem(self, item):
        self._item = item

    def getItem(self):
        return item

    def updateBlock(self):
        surfBack = pygame.Surface((self._width, self._height))
        if self._selected:
            surfBack.fill(self._selectedBorder)
        else:
            surfBack.fill(self._borderColor)
        surfBack.set_alpha(self._transparency)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)
        surf.set_alpha(self._transparency)

        if self._item != None:
            image = self._item.getImage()
            surf.blit(image,(self._width//2 - self._item.getWidth()//2,
                             self._height//2 - self._item.getHeight()//2))
        
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
