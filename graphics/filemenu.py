import pygame, glob
from polybius.graphics import Button, ScrollSelector, TextInput
from polybius.graphics.utils import Window, AbstractGraphic

class FileMenu(AbstractGraphic, Window):

    def __init__(self, pos, dimensions, menuType="Load"):

        AbstractGraphic.__init__(self, pos)
        Window.__init__(self)

        self._type = menuType
        self._pos = pos
        self._offset = (pos[0], pos[1])

        self._width  = dimensions[0]
        self._height = dimensions[1]

        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._smallFont = pygame.font.SysFont("Times New Roman", 14)
        self._borderColor = (0,0,0)
        self._borderWidth = 2
        self._backgroundColor = (80,80,80)

        self._buttonWidth  = 3 * (self._width // 4)
        self._buttonHeight = (self._height-30) // 5

        self._buttonXpos = self._width//2 - self._buttonWidth // 2
        self._buttonYpos = (self._height - self._buttonHeight) - 15

        self._loadButton = Button(menuType, (self._buttonXpos,self._buttonYpos),
                                    self._font, backgroundColor=(0,255,0),
                                    dims=(self._buttonWidth//2, self._buttonHeight),
                                    borderColor=(0,0,0), borderWidth=2)

        self._cancelButton = Button("Cancel", (self._buttonXpos+self._buttonWidth//2, self._buttonYpos),
                                    self._font, backgroundColor=(120,120,150),
                                    dims=(self._buttonWidth//2, self._buttonHeight),
                                    borderColor=(0,0,0), borderWidth=2)

        

        self._textbox = TextInput((self._buttonXpos,self._buttonYpos - (25 + 10)),
                                  self._smallFont, (self._buttonWidth, 30),
                                  maxLen = 25)
        self._selection = None

        self.updateGraphic()

    def createFileSelect(self):
        filePath = "saves/"
        fileExtension = ".sqs"
        self._options = []
        for file in glob.glob("saves/*.sqs"):
            fileName = file[len(filePath):][:-len(fileExtension)]
            d = {"text":fileName, "func":self.updateSelection, "args":fileName}
            self._options.append(d)
        xpos = self._pos[0]+3+self._buttonXpos
        ypos = self._pos[1]+40
        pos = (xpos, ypos)
        dims = (self._buttonWidth,self._buttonHeight*2.75)
        self._fileSelect = ScrollSelector(pos,dims,30,self._options,(0,0,0))

    def handleEvent(self, event, cancelFunc=None):
        """Handles events on the pause menu"""
        self._loadButton.handleEvent(event, self.load, offset=self._offset)
        self._cancelButton.handleEvent(event, self.cancel, args=(cancelFunc,), offset=self._offset)
        self._fileSelect.handleEvent(event)
        if self._type == "Save":
            self._textbox.handleEvent(event, offset=self._offset)
        self.updateGraphic()
        return self.getSelection()

    def updateSelection(self, text):
        self._textbox.setText(text)
        self.updateGraphic()

    def load(self):
        """Sets the selection to resume""" 
        self._selection = self._textbox.getInput()
        self._textbox.setText("")
        self.close()

    def display(self):
        Window.display(self)
        self.createFileSelect()

    def cancel(self, func):
        """Sets the selecton to controls"""
        func()
        self._textbox.setText("")
        self.close()

    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def draw(self, surf):
        AbstractGraphic.draw(self, surf)
        self._fileSelect.draw(surf)

    def internalUpdate(self, surf):
        """Updates the display of the pause menu"""
        self._loadButton.draw(surf)
        self._cancelButton.draw(surf)
        self._textbox.draw(surf)
        
