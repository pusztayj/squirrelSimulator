
class Level():

    def __init__(self):
        self._active = True

    def isActive(self):
        return self._active

    def setActive(self, boolean):
        self._active = boolean
