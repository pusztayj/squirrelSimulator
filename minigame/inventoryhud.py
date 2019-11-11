
import pygame
from modules.drawable import Drawable
from modules.frameManager import FRAMES
from items.items import Spear

class InventoryHUD(Drawable):

    def __init__(self, pos, dimensions, player):
        super().__init__("", pos, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._player = player
        self._items = [item for item in self._player.getInventory()]
        self._selected = 0
        self._blocks = []
        for x in range(9):
            if x < len(self._items):
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=self._items[x],
                              selected=x==self._selected)
            else:
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=None,
                              selected=x==self._selected)
            self._blocks.append(i)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            # Check if the keys 1 through 9 were pressed
            if event.key in [x for x in range(49,58)]:
                self._selected = event.key - 49
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self._selected = (self._selected + 1) % 9
            if event.button == 5:
                self._selected = (self._selected - 1) % 9
            if event.button == 1:
                for i, b in enumerate(self._blocks):
                    if b.getCollideRect().collidepoint(event.pos):
                        self._selected = i
                    

    def update(self):
        self._items = [item for item in self._player.getInventory()]
        self._blocks = []
        for x in range(9):
            if x < len(self._items):
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=self._items[x],
                              selected=x==self._selected)
            else:
                i = ItemBlock((self._position[0]+(x*(self._width//9)),
                           0+self._position[1]),
                          (self._width//9,self._height),item=None,
                              selected=x==self._selected)
            self._blocks.append(i)
        
    def draw(self, screen):
        # Draw the background
        for block in self._blocks:
            block.draw(screen)


class ItemBlock(Drawable):

    def __init__(self, pos, dimensions, item=None, selected=False):
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
