class Command(object):

    def __init__(self, func, args=()):
        self._func = func
        self._args = args

    def execute(self):
        return self._func(*self._args)
