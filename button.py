
import pygame
from drawable import Drawable
from textbox import TextBox

class Button(Drawable):

    def __init__(self, text, position, font, color, backgroundColor,
                 height, width, borderColor=(0,0,0), borderWidth=0):
        super().__init__("", position, worldBound=False)
        self._fontColor = color
        self._font = font
        self._backgroundColor = backgroundColor
        self._text = text
        self._height = height
        self._width = width
        self._borderColor = borderColor
        self._borderWidth = borderWidth

        # Default button colors
        self._defaultFontColor = color
        self._defaultBackgroundColor = backgroundColor
        
        # Store custom highlighting and click formating here...
        
        self.__updateButton()

    def setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor
        self.__updateButton()

    def setText(self, text):
        self._text = text
        self.__updateButton()

    def setFont(self, font):
        self._font = font
        self.__updateButton()

    def setFontColor(self, color):
        self._fontColor = color

    def setBorderColor(self, color):
        self._borderColor = borderColor

    def setBorderWidth(self, width):
        self._borderWidth = width

    def buttonPressed(self):
        (r,g,b) = self._defaultFontColor
        if r < 215: r += 40
        else: r =255
        if g < 215: g += 40
        else: g =255
        if b < 215: b += 40
        else: b =255
        self._fontColor = (r,g,b)
        (r,g,b) = self._defaultBackgroundColor
        if r < 235: r += 20
        else: r =255
        if g < 235: g += 20
        else: g =255
        if b < 235: b += 20
        else: b =255
        self._backgroundColor = (r,g,b)
        self.__updateButton()

    def buttonReleased(self):
        self._backgroundColor = self._defaultBackgroundColor
        self._fontColor = self._defaultFontColor
        self.__updateButton()

    def move(self, event, func, *args, offset=(0,0)):
        rect = self.getCollideRect()
        rect = rect.move(offset[0],offset[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: 
            if rect.collidepoint(event.pos):
                self.buttonPressed()
                func(*args)
        elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                self.buttonReleased()
        elif rect.collidepoint(pygame.mouse.get_pos()):
            self.setHover()
        else:
            self.removeHover()
                
    def setHover(self):
        (r,g,b) = self._defaultBackgroundColor
        if r > 40: r -= 40
        else: r = 0
        if g > 40: g -= 40
        else: g = 0
        if b > 40: b -= 40
        else: b = 0
        self._backgroundColor = (r,g,b)
        self.__updateButton()

    def removeHover(self):
        self._backgroundColor = self._defaultBackgroundColor
        self.__updateButton()
    
    def __updateButton(self):
        """Update the textbox after parameters have been changed"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)
        t = TextBox(self._text, (0,0), self._font, self._fontColor)
        y_pos = (self._height // 2) - (t.getHeight() // 2)
        x_pos = (self._width // 2) - (t.getWidth() // 2)
        t.setPosition((x_pos, y_pos))
        t.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
