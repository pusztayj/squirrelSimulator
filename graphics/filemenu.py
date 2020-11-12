import pygame, glob
from polybius.graphics import Button, ScrollSelector, TextInput
from polybius.graphics.utils import Window, AbstractGraphic

class FileMenu(AbstractGraphic, Window):

    def __init__(self, pos, dimensions, menuType="Load"):

        AbstractGraphic.__init__(self, pos)
        Window.__init__(self)

        self._type = menuType

        self._offset = (pos[0], pos[1])

        self._width  = dimensions[0]
        self._height = dimensions[1]

        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._smallFont = pygame.font.SysFont("Times New Roman", 14)
        self._borderColor = (0,0,0)
        self._borderWidth = 2
        self._backgroundColor = (80,80,80)

        buttonWidth  = 3 * (self._width // 4)
        buttonHeight = (self._height-30) // 5

        buttonXpos = self._width//2 - buttonWidth // 2
        buttonYpos = (self._height - buttonHeight) - 15

        self._loadButton = Button(menuType, (buttonXpos,buttonYpos),
                                    self._font, (0,0,0), (0,255,0),
                                    buttonHeight, buttonWidth//2, (0,0,0), 2)

        self._cancelButton = Button("Cancel", (buttonXpos+buttonWidth//2, buttonYpos),
                                    self._font, (0,0,0), (120,120,150),
                                    buttonHeight, buttonWidth//2, (0,0,0), 2)

        filePath = "saves/"
        fileExtension = ".sqs"
        self._options = []
        for file in glob.glob("saves/*"):
            fileName = file[len(filePath):][:-len(fileExtension)]
            d = {"text":fileName, "func":self.updateSelection, "args":fileName}
            self._options.append(d)
        self._levelSelect = ScrollSelector((pos[0]+3+buttonXpos,pos[1]+45),(buttonWidth,buttonHeight*2.75),
                                           30,self._options,(0,0,0))

        self._textbox = TextInput((buttonXpos,buttonYpos - (25 + 10)),
                                  self._smallFont, (buttonWidth, 25),
                                  maxLen = 25)
        self._selection = None

        self.updateGraphic()

    def handleEvent(self, event):
        """Handles events on the pause menu"""
        self._loadButton.handleEvent(event, self.load, offset=self._offset)
        self._cancelButton.handleEvent(event, self.cancel, offset=self._offset)
        self._levelSelect.handleEvent(event)
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

    def cancel(self):
        """Sets the selecton to controls"""
        self._textbox.setText("")
        self.close()

    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def draw(self, surf):
        AbstractGraphic.draw(self, surf)
        self._levelSelect.draw(surf)

    def internalUpdate(self, surf):
        """Updates the display of the pause menu"""
        self._loadButton.draw(surf)
        self._cancelButton.draw(surf)
        self._textbox.draw(surf)
        
