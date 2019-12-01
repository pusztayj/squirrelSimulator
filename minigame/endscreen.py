import pygame
from graphics import *
from animals import *
from minigame.threexthreeinventory import threeXthreeInventory


class EndScreen(object):

    def __init__(self,screensize,player):
        self._screensize = screensize
        self._player = player
        self._font = pygame.font.SysFont("Times New Roman", 28)

        self._text = TextBox("You died. Below are your stats: ",
                             (0,0),self._font,(255,255,255))

        self._text.setPosition(((self._screensize[0]-self._text.getWidth())//2,
                                self._screensize[1]//5))


        self._inventory = threeXthreeInventory(((screensize[0]//4)-50,150),
                                               (300,200), self._player)

        self._xpText = TextBox("XP: "+str(self._player.getXP()),
                               (600,150),self._font,(255,255,255))

        y = self._xpText.getHeight()
        self._acornsText = TextBox("Acorns: "+str(self._player.getAcorns()),
                               (600,150+y+5),self._font,(255,255,255))
        y+=self._acornsText.getHeight()
        pack = self._player.getPack().getMembers()
        followers = [x.getName() for x in pack if x!=None]
        followersStr = ', '.join(followers)
        self._followerText = TextBox("Followers: "+followersStr,
                               (600,150+y+5),self._font,(255,255,255))

        y+=self._followerText.getHeight()
        self._scoreText = TextBox("Score: "+str(self.score()),
                               (600,150+y+5),self._font,(255,255,255))

        # Buttons

        self._restartButton = Button("Restart",(800,150),self._font,
                                     (255,255,255),(222,44,44),50,100,
                                     borderWidth = 2)
        self._exitButton = Button("Exit",(800,202),self._font,(255,255,255),
                                     (46,46,218), 50,100,borderWidth = 2)
        

    def score(self):
        inventoryWorth = sum([x.getValue() for x in self._player.getInventory()])
        followers = len([x.getName() for x in self._player.getPack().getMembers() if x!=None])
        score = inventoryWorth + self._player.getAcorns() + (5*self._player.getXP()) +\
             (100*followers)
        return score

    def draw(self,screen):
        self._text.draw(screen)
        self._inventory.draw(screen)
        self._xpText.draw(screen)
        self._acornsText.draw(screen)
        self._followerText.draw(screen)
        self._scoreText.draw(screen)
        self._restartButton.draw(screen)
        self._exitButton.draw(screen)

        
                                

        
