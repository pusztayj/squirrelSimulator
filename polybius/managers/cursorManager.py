
import pygame

class CursorManager():

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._CM()
        return cls._INSTANCE

    class _CM():

        def __init__(self):

            self._cursors = {"pointer":pygame.SYSTEM_CURSOR_ARROW,
                             "ibeam":pygame.SYSTEM_CURSOR_IBEAM,
                             "wait":pygame.SYSTEM_CURSOR_WAIT,
                             "crosshair":pygame.SYSTEM_CURSOR_CROSSHAIR,
                             "small_wait":pygame.SYSTEM_CURSOR_WAITARROW,
                             "nwse":pygame.SYSTEM_CURSOR_SIZENWSE,
                             "nesw":pygame.SYSTEM_CURSOR_SIZENESW,
                             "ew":pygame.SYSTEM_CURSOR_SIZEWE,
                             "ns":pygame.SYSTEM_CURSOR_SIZENS,
                             "all_directions":pygame.SYSTEM_CURSOR_SIZEALL,
                             "no":pygame.SYSTEM_CURSOR_NO,
                             "hand":pygame.SYSTEM_CURSOR_HAND}

            self._default = "pointer"
            self._visible = True
            self._current = self._default

        def getCursorName(self):
            return self._current

        def getCursor(self):
            return self._cursors[self._current]

        def setCursor(self, cursor):
            default = self._cursors[self._default]
            newCursor = self._cursors.get(cursor, default)
            pygame.mouse.set_cursor(newCursor)
            self._current = cursor

        def setToDefault(self):
            pygame.mouse.set_cursor(self._cursors[self._default])
            self._current = self._default

        def getPosition(self, offset=(0,0)):
            m_pos = pygame.mouse.get_pos()
            m_pos = (m_pos[0] - offset[0],
                     m_pos[1] - offset[1])
            return m_pos

        def addCursor(self, cursorName, cursor):
            self._cursors[cursorName] = cursor

        def makeVisible(self):
            pygame.mouse.set_visible(True)
            self._visible = True

        def makeInvisible(self):
            pygame.mouse.set_visible(False)
            self._visible = False

        def isVisible(self):
            return self._visible


CURSOR = CursorManager.getInstance()
