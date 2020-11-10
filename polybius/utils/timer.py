class Timer:

    def __init__(self, initialTime):

        # Assert that the initialTime is an int or a function
        assert type(initialTime) in (int, float) or callable(initialTime)

        # If initialTime is a function, assert that it returns an int
        assert not callable(initialTime) or type(initialTime()) in (int, float)

        self._initialTime = initialTime

        # Wrap initialTime in a function if it's a number
        if type(initialTime) in [int, float]:
            self._initialTime = lambda: initialTime
            
        self._timer = self._initialTime()

    def resetTimer(self):
        self._timer = self._initialTime()

    def update(self, ticks, func):
        self._timer -= ticks
        if self._timer <= 0:
            func()
            self.resetTimer()
