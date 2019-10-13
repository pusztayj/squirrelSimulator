import pygame
from modules.drawable import Drawable
from graphics.banner import Banner

class ScrollBox(Drawable):

    def __init__(self, position, dimensions, internalSurface,
                 borderColor=(0,0,0), borderWidth=0):
        super().__init__("", position, worldBound=False)
        self._height = dimensions[0]
        self._width = dimensions[1]
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._internalSurface = internalSurface
        
        self._sidebarWidth = 10
        self._sidebarColor = (120,120,120)
        if self._height > self._internalSurface.getHeight():
            self._sliderHeight = self._height
        else:
            self._sliderHeight = (self._height ** 2) // \
                                 self._internalSurface.getHeight()
        self._sliderColor = (180,180,180)

        # Used to allow the scrollbox to appear around the screen
        self._offset = position

        self._currentOffset = 0

        # Calculate slide step
        self._step = self._internalSurface.getHeight() // self._height

        self._scrollOffset = 0

        self._slider = Banner((self._width-self._sidebarWidth,0),self._sliderColor,
                         (self._sliderHeight,self._sidebarWidth))

        self._scrolling = False
        
        self.updateScrollBox()

    def getOffset(self):
        return self._currentOffset

    def getInternalSurface(self):
        return self._internalSurface

    def setInternalSurface(self, surface):
        self._internalSurface.update(surface)

    def dragSlider(self):
        if self._scrolling:
            prevY = self._slider.getY()
            x,y = pygame.mouse.get_pos()
            y -= self._offset[1]

            # Check that the slider bar has not reached the top or bottom of the window
            if (prevY - y > 0 and self._slider.getY() >= 0) or \
                    (prevY - y < 0 and \
                    self._slider.getY() + self._sliderHeight < self._height):

                # Update the slider's position
                self._slider.setPosition((self._slider.getX(), min(self._height - self._slider.getHeight(),
                                                                   max(0,y))))
                # Update the scroll offset
                self._scrollOffset = prevY - y

                # Set the position of the internal surface according to the offset
                self._internalSurface.setPosition((self._internalSurface.getX(),
                                      max(-1 * self._internalSurface.getHeight() - self.getHeight(),
                                          min(0, self._internalSurface.getY() +
                                      self._scrollOffset * self._step))))

                # Update the current Offset
                self._currentOffset += self._scrollOffset * self._step

                # Update the scroll box
                self.updateScrollBox()

    def move(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            ex,ey = event.pos
            ox,oy = self._offset
            pos = (ex-ox, ey-oy)
            if self._slider.getCollideRect().collidepoint(pos):
                self._scrolling = True
        if event.type == pygame.MOUSEBUTTONUP and event.button==1:
            self._scrolling = False            
        self.dragSlider()
    
    def updateScrollBox(self):
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        displaySurf = pygame.Surface((self._width, self._height))
        if issubclass(type(self._internalSurface), Drawable): 
            self._internalSurface.draw(displaySurf)
        sideBar = Banner((self._width-self._sidebarWidth,0),self._sidebarColor,
                         (self._height,self._sidebarWidth))
        sideBar.draw(displaySurf)
        self._slider.draw(displaySurf)
        surfBack.blit(displaySurf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
