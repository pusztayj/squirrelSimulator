import pygame, string
from polybius.utils import EventWrapper 

class KeyIdentifier():

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        """Used to obtain a singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._KI()
        return cls._INSTANCE

    class _KI():

        def __init__(self):

            self._symbolKeys = [ord(p) for p in string.punctuation]

            # Initialize the symbol dictionary
            self._symbols = {}

            # Get the key IDs from pygame
            numKeys = [eval("pygame.K_%d" % (i,)) for i in range(10)]
            numPadKeys = [eval("pygame.K_KP%d" % (i,)) for i in range(10)]
            alphaKeys = [eval("pygame.K_%s" % (chr(i+97),)) for i in range(26)]

            # Add digits to the dictionary
            for x in range(10):
                self._symbols[EventWrapper(pygame.KEYDOWN, numKeys[x])] = str(x)
                self._symbols[EventWrapper(pygame.KEYDOWN, numPadKeys[x],
                                           [pygame.KMOD_NUM])] = str(x)

            # Add symbols to the dictionary
            for i, s in enumerate(")!@#$%^&*("):
                self._symbols[EventWrapper(pygame.KEYDOWN, numKeys[i],
                                           [pygame.KMOD_SHIFT])] = s

            # Add letters to the dictionary
            for i in range(26):
                self._symbols[EventWrapper(pygame.KEYDOWN, alphaKeys[i])] = chr(97+i)
                self._symbols[EventWrapper(pygame.KEYDOWN, alphaKeys[i], [pygame.KMOD_SHIFT])] = chr(i+65)
                self._symbols[EventWrapper(pygame.KEYDOWN, alphaKeys[i], [pygame.KMOD_CAPS])] = chr(i+65)
                
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_LEFTBRACKET)] = "["
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_BACKSLASH)] = "\\"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_RIGHTBRACKET)] = "]"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_COMMA)] = ","
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_PERIOD)] = "."
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SLASH)] = "/"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SEMICOLON)] = ";"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_QUOTE)] = "'"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_BACKQUOTE)] = "`"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_EQUALS)] = "="
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_MINUS)] = "-"
            
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_COMMA, [pygame.KMOD_SHIFT])] = "<"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_PERIOD, [pygame.KMOD_SHIFT])] = ">"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SLASH, [pygame.KMOD_SHIFT])] = "?"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_LEFTBRACKET, [pygame.KMOD_SHIFT])] = "{"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_RIGHTBRACKET, [pygame.KMOD_SHIFT])] = "}"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_EQUALS, [pygame.KMOD_SHIFT])] = "+"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_BACKQUOTE, [pygame.KMOD_SHIFT])] = "~"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_BACKSLASH, [pygame.KMOD_SHIFT])] = "|"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_QUOTE, [pygame.KMOD_SHIFT])] = '"'
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SEMICOLON, [pygame.KMOD_SHIFT])] = ":"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_MINUS, [pygame.KMOD_SHIFT])] = "_"

            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PLUS)] = "+"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MINUS)] = "-"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_DIVIDE)] = "/"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MULTIPLY)] = "*"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PERIOD)] = "."
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SPACE)] = " "

            self._wrappers = [w for w in self._symbols.keys()]
            self._wrappers.sort(key=lambda x: len(x.getMods()))
            self._wrappers.reverse()

        def getChar(self, event):     
            for wrapper in self._wrappers:
                if wrapper.check(event):
                    return self._symbols[wrapper]
            return ""

KEY_IDENTIFIER = KeyIdentifier.getInstance()
