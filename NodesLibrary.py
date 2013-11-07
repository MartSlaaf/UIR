import random

#this is list of classes in strange state.
LIST_OF_FUNCTIONS = ['NodeFunction', 'StrangeFunction', 'VariousFunction']


class NodeFunction():
    def __init__(self):
        self._firstParam = random.randint(-100, 100)
        self._secondParam = random.randint(1, 10)

    def evalMe(self, inp):
        outp = inp * self._firstParam / self._secondParam
        return outp


class StrangeFunction():
    def __init__(self):
        self._firstParam = random.randint(-100, 100)
        self._secondParam = random.randint(1, 10)

    def evalMe(self, inp):
        outp = inp * self._firstParam / (self._secondParam * self._secondParam)
        return outp


class VariousFunction():
    def __init__(self):
        self._firstParam = random.randint(-100, 100)
        self._secondParam = random.randint(1, 10)

    def evalMe(self, inp):
        outp = inp * self._firstParam / (self._secondParam * 3.1415926)
        return outp
