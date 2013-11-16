import random
import xml.etree.ElementTree as ElementTree
import numpy as np
from math import fabs
#this is list of classes in strange state.
LIST_OF_FUNCTIONS = ['NoFilter', 'DiscrDiff', 'MedianFilter', 'EvenNoise', 'MovingAverage']


class GeneralNodeFunction():
    """
    def __init__(self):
        self.params = {'frame': 10, 'crime': 12}

    def eval_me(self, inp):
        outp = inp * self.params['frame'] / self.params['crime']
        return outp
    """

    def store_xml(self):
        return '<node function="' + str(self.__class__.__name__) + '" enter_params="' + str(self.params) + '"/>\n'


class NoFilter(GeneralNodeFunction):
    """
    Looks like filter, but doing nothing.
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        print 'nothing' , len(inp)
        return inp


class DiscrDiff(GeneralNodeFunction):
    """
    (Y(i+1)-Y(i))
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        print 'DiscrDiff' , len(inp)
        outp = [0]
        for iteration in range(len(inp) - 1):
            outp.append(inp[iteration + 1] - inp[iteration])
        return outp


class DiscrDiffRel(GeneralNodeFunction):
    """
    (Y(i+1)-Y(i))/Y(i)
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
        print 'DiscrDiffRel' , len(inp)
        outp = [0]
        for iteration in range(len(inp) - 2):
            outp.append((inp[iteration + 1] - inp[iteration]) / (
            (fabs(inp[iteration]) + 1) *  1))
        return outp


class MedianFilter(GeneralNodeFunction):
    """
    Median filter with frame randomly 3 or 5.
    """

    def __init__(self):
        random.seed()
        self.params = {'frame': random.randint(1, 1) * 2 + 1}

    def _middle(self, a, b, c):
        if (a <= b) and (a <= c):
            middle = b if b <= c else c
        elif (b <= a) and (b <= c):
            middle = a if a <= c else c
        else:
            middle = a if a <= b else b
        return middle


    def eval_me(self, inp):
        print 'MedianFilter' , len(inp)
        border = int((self.params['frame'] - 1) / 2)
        outp = []
        for it in range(border):
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
        self.params = {}
        self.params['frame'] = random.randint(0, 5)

    def eval_me(self, inp):
        print 'EvenNoise' , len(inp)
        for iter in range(len(inp) - 1):
            inp[iter] += (random.random() - 0.5) * self.params['frame']
        return inp


class MovingAverage(GeneralNodeFunction):
    def __init__(self):
        random.seed()
        self.params = {}
        self.params['window'] = random.randint(3, 8)

    def _runningMeanFast(self, x, N):
        return np.convolve(x, np.ones((N,)) / N)[(N - 1):]

    def eval_me(self, inp):
        print 'MovingAverage', len(inp)
        border = int((self.params['window'] - 1) / 2)
        for it in range(border - 1):
            inp.insert(0, inp[0])
            inp.append(inp[-1])
        outp = self._runningMeanFast(inp, self.params['window'])
        return list(outp)
