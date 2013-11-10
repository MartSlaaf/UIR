import random
import xml.etree.ElementTree as ElementTree
import numpy as np

#this is list of classes in strange state.
LIST_OF_FUNCTIONS = ['NodeFunction', 'StrangeFunction', 'VariousFunction']


class GeneralNodeFunction():
    """
    def __init__(self):
        self.params = {'frame': 10, 'crime': 12}

    def eval_me(self, inp):
        outp = inp * self.params['frame'] / self.params['crime']
        return outp
    """

    def store_xml(self, parent):
        ElementTree.SubElement(parent, self.__class__.__name__, attrib=self.params)


class NoFilter(GeneralNodeFunction):
    """
    Looks like filter, but doing nothing.
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        return inp


class DiscrDiff(GeneralNodeFunction):
    """
    (Y(i+1)-Y(i))
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        outp = []
        for iteration in range(len(inp) - 2):
            outp.append(inp[iteration + 1] - inp[iteration])
        return outp


class DiscrDiffRel(GeneralNodeFunction):
    """
    (Y(i+1)-Y(i))/Y(i)
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        outp = []
        for iteration in range(len(inp) - 2):
            outp.append((inp[iteration + 1] - inp[iteration]) / inp[iteration])
        return outp


class MedianFilter(GeneralNodeFunction):
    """
    Median filter with frame randomly 3 or 5.
    """

    def __init__(self):
        random.seed()
        self.params = {'frame': random.randint(1, 2) * 2 + 1}

    def _middle(self, a, b, c):
        if (a <= b) and (a <= c):
            middle = b if b <= c else c
        elif (b <= a) and (b <= c):
            middle = a if a <= c else c
        else:
            middle = a if a <= b else b
        return middle


    def eval_me(self, inp):
        border = int((self.params['frame'] - 1) / 2)
        outp = []
        for it in range(border - 1):
            inp.insert(0, inp[0])
            inp.append(inp[-1])
        for step in range(len(inp) - (border + 1)):
            outp.append(self._middle(inp[step], inp[step + 1], inp[step + 2]))
        return outp


class EvenNoise(GeneralNodeFunction):
    """
    Addind to the signal random noise in selected frame
    """
    def __init__(self):
        random.seed()
        self.frame = random.randint(0, 100)

    def eval_me(self, inp):
        for iter in range(len(inp) - 1):
            inp[iter] += (random.random() - 0.5) * self.frame
        return inp

class MovingAverage(GeneralNodeFunction):
    def __init__(self):
        random.seed()
        self._window = random.randint(3,8)

    def _runningMeanFast(self, x, N):
        return np.convolve(x, np.ones((N,))/N)[(N-1):]

    def eval_me(self, inp):
        outp = self._runningMeanFast(inp,self._window)
