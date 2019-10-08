
class Buff():

    def __init__(self, target, duration):

        self._target = target
        self._duration = duration
        self._timeLeft = duration
        self._expired = False

    def decrementDuration(self):
        self._timeLeft -= 1
        if self._timeLeft == 0:
            self._expired = True

    def getTimeLeft(self):
        return self._timeLeft

    def expire(self):
        self._expired = True

    def expired(self):
        return self._expired

    def setTarget(self, target):
        self._target = target
        
    def __repr__(self):
        return "Type:     " + type(self).__name__ + \
               "\nDuration: " + str(self._timeLeft) + "/" + str(self._duration)

class Poison(Buff):

    def __init__(self, target=None, duration=10):
        super().__init__(target, duration)

    def applyBuff(self):
        self._target.loseHealth(2)
        self.decrementDuration()

class Ticks(Buff):

    def __init__(self, target=None, duration=100):
        super().__init__(target, duration)

    def applyBuff():
        self._target.loseHealth(1)
        self.decrementDuration()

class PotionOfHealing(Buff):

    def __init__(self):
        pass

    def applyBuff():
        pass

class Bleeding(Buff):

    def __init__(self):
        pass

    def applyBuff():
        pass
