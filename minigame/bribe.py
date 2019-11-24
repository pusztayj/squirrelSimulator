
import pygame
from graphics import *

class Bribe(Window):

    def __init__(self, player, entity, SCREEN_SIZE):
        
        Window.__init__(self)

        self._player = player
        self._entity = entity

        # Style Attributes
        self._position = (SCREEN_SIZE[0]//2 - 225//2,100)
        self._font = pygame.font.SysFont("Times New Roman", 22)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._width = 225
        self._height = 100
        self._borderWidth = 2
        self._borderColor = (0,0,0)
        self._backgroundColor = (139,79,59)

        givePos = (self._position[0] + 30, self._position[1] + 55)
        self._giveButton = Button("Give", givePos, self._font, (0,0,0),
                                  (0,120,0), 25, 75, (0,0,0), 2)
        cancelPos = (self._position[0] + 115, self._position[1] + 55)
        self._cancelButton = Button("Cancel", cancelPos, self._font, (0,0,0),
                                  (200,0,0), 25, 75, (0,0,0), 2)
        acornPos = (self._position[0] + 25, self._position[1] + 20)
        self._acorns = TextBox("Acorns: ", acornPos, self._font, (0,0,0))
        acornAvailPos = (self._position[0] + 165, self._position[1] + 20)
        self._acornsAvailable = TextBox("/ " + str(player.getAcorns()),
                               acornAvailPos, self._font, (0,0,0))
        bribePos = (self._position[0] + 105, self._position[1] + 22)
        self._bribeAcorns = TextInput(bribePos, self._font, (50,20),
                                      numerical=True, defaultText="0",
                                      clearOnActive=True,borderWidth=1)

        self._popupWindow = PopupWindow("", (0,0), (285,100), self._font,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((SCREEN_SIZE[0]//2 - self._popupWindow.getWidth()//2,
                                       SCREEN_SIZE[1]//3 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

    def handleEvent(self, event):
        if self._popupWindow.getDisplay():
            self._popupWindow.handleEvent(event)
        else:
            self._giveButton.handleEvent(event, self.executeBribe)
            self._cancelButton.handleEvent(event, self.close)
            self._bribeAcorns.handleEvent(event)


    def executeBribe(self):
        bribe = self._bribeAcorns.getInput()
        if bribe.isdigit():
            bribe = int(bribe)
            if bribe == 0:
                self._popupWindow.setText("You are not giving any Acorns")
                self._popupWindow.display()
            elif self._player.getAcorns() < bribe:
                self._popupWindow.setText("You do not have the Acorns")
                self._popupWindow.display()
            else:
                friendBoost = bribe * 0.5 # 2 Acorns = 1 Friend Point
                self._player.setAcorns(self._player.getAcorns() - bribe)
                self._entity.setAcorns(self._entity.getAcorns() + bribe)
                self._entity.changeFriendScore(friendBoost)
                self._popupWindow.setText(self._entity.getName() + " is pleased")
                self._popupWindow.display()  

    def draw(self, screen):
        
        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        screen.blit(surfBack, self._position)
        
        # Draw widgets
        self._cancelButton.draw(screen)
        self._giveButton.draw(screen)
        self._bribeAcorns.draw(screen)
        self._acornsAvailable.draw(screen)
        self._acorns.draw(screen)
        if self._popupWindow.getDisplay():
            self._popupWindow.draw(screen)

    def update(self):
        self._acornsAvailable.setText("/ " + str(self._player.getAcorns()))
        
