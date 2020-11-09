

class Callable():

    def __init__(self, func, args=tuple()):

        self._func = func
        self._args = args

    def call(self):
        self._func(*self._args)
