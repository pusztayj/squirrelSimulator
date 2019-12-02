import pygame, random
from modules import *
from graphics import *
from animals import *
from minigame.threexthreeinventory import threeXthreeInventory


class EndScreen(object):

    def __init__(self,screensize,player):

        self._songs = ["death.mp3"]
        self._currentSong = random.choice(self._songs)

        # background
        self._background = Drawable("merchantForest2.png", Vector2(0,0), worldBound=False)
        
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
        followers = [x.getName() for x in pack if x!=None and x!=self._player]
        followersStr = ', '.join(followers)
        self._followerText = TextBox("Followers: "+followersStr,
                               (600,150+y+5),self._font,(255,255,255))

        y+=self._followerText.getHeight()
        self._scoreText = TextBox("Score: "+str(self.score()),
                               (600,150+y+5),self._font,(255,255,255))

        # Buttons

        self._restartButton = Button("Restart",((screensize[0]//4)-30,400),self._font,
                                     (255,255,255),(222,44,44),50,100,
                                     borderWidth = 2)
        self._exitButton = Button("Exit",((((screensize[0]//4)+250)-120),400),self._font,(255,255,255),
                                     (46,46,218), 50,100,borderWidth = 2)

        self._selection = None

        SoundManager.getInstance().playMusic(self._currentSong)
        

    def score(self):
        inventoryWorth = sum([x.getValue() for x in self._player.getInventory()])
        followers = len([x.getName() for x in self._player.getPack().getMembers() if x!=None and x!=self._player])
        score = inventoryWorth + self._player.getAcorns() + (5*self._player.getXP()) +\
             (100*followers)
        return score

    def handleEvent(self, event):
        self._restartButton.handleEvent(event, self.restart)
        self._exitButton.handleEvent(event, self.leaveGame)
        return self.getSelection()

    def leaveGame(self):
        self._selection = 0

    def restart(self):
        self._selection = 1

    def getSelection(self):
        sel = self._selection
        self._selection = None
        return sel

    def draw(self,screen):
        self._background.draw(screen)
        self._text.draw(screen)
        self._inventory.draw(screen)
        self._xpText.draw(screen)
        self._acornsText.draw(screen)
        self._followerText.draw(screen)
        self._scoreText.draw(screen)
        self._restartButton.draw(screen)
        self._exitButton.draw(screen)

    def update(self):
        if not pygame.mixer.music.get_busy():
            temp = self._currentSong
            while temp == self._currentSong:
                self._currentSong = random.choice(self._songs)
            SoundManager.getInstance().playMusic(self._currentSong)
        
                                

        
