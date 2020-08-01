"""
Author: Trevor Stalnaker
File: statdisplay.py

A class that creates a display for the player's stats
"""

from polybius.graphics import Drawable, ProgressBar, TextBox
from economy.acorn import Acorn
import pygame

digitLen = {1:33, 2:38, 3:45, 4:55}

class StatDisplay(Drawable):

    def __init__(self, position, entity):
        """Initializes the stats display"""
        super().__init__("", position, worldBound=False)
        self._entity = entity
        self._width = 200
        self._height = 75
        self._borderWidth = 2
        self._borderColor = (0,0,0)
        self._backgroundColor = (120,120,220)
        self._nameFont = pygame.font.SysFont("Times New Roman", 20)
        self._font = pygame.font.SysFont("Times New Roman", 15)
        self._fontColor = (255,255,255)

        # Create Progress Bars
        self._healthBar = ProgressBar((60,25), 5*(self._width//8),
                                      entity.getBaseHealth(),
                                      entity.getHealth())
        self._hungerBar = ProgressBar((60,40), 5*(self._width//8),
                                        entity.getBaseHunger(),
                                        entity.getHunger(),
                                        barColor=(235,125,52))
        self._staminaBar = ProgressBar((60,55), 5*(self._width//8),
                                        entity.getBaseStamina(),
                                        entity.getStamina(),
                                        barColor=(0,0,255))
        # Create Text Boxes
        self._nameDisplay = TextBox(entity.getName(), (5,0),
                                    self._nameFont, self._fontColor)
        self._healthLabel = TextBox("Health",(5,22), self._font,
                                    self._fontColor)
        self._hungerLabel = TextBox("Hunger",(5,37), self._font,
                                    self._fontColor)
        self._staminaLabel = TextBox("Stamina",(5,52), self._font,
                                     self._fontColor)
        self._acornCount = TextBox("", (self._width-50, 4),
                                       self._font, self._fontColor)

        # Save an image of the entity and of an acorn
        self._entityImage = entity.getImage()
        acorn = Acorn((0,0))
        acorn.scale(.5)
        self._acornImage = acorn.getImage()

        self.update()

    def update(self):
        """Update the stats display as the player's attributes change"""
        
        # Update the players name incase it changed
        self._nameDisplay = TextBox(self._entity.getName(), (5,0),
                                    self._nameFont, self._fontColor)
                
        surfBack = pygame.Surface((self._width + (self._borderWidth * 2),
                                   self._height + (self._borderWidth * 2)))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)

        # Draw Widgets on the Surface
        self._healthBar.setProgress(self._entity.getHealth())
        self._healthBar.draw(surf)
        self._hungerBar.setProgress(self._entity.getHunger())
        self._hungerBar.draw(surf)
        self._staminaBar.setProgress(self._entity.getStamina())
        self._staminaBar.draw(surf)
        self._nameDisplay.draw(surf)
        self._healthLabel.draw(surf)
        self._hungerLabel.draw(surf)
        self._staminaLabel.draw(surf)

        acorns = str(self._entity.getAcorns())
        self._acornCount.setText(acorns)
        self._acornCount.setPosition((self._width - digitLen[len(acorns)], 4))
        
        self._acornCount.draw(surf)

        # Blit images to the display
        surf.blit(self._acornImage, (self._width-25, 5))
        
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
