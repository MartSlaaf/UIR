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
        return inp


class DiscrDiff(GeneralNodeFunction):
    """
    (Y(i+1)-Y(i))
    """

    def __init__(self):
        self.params = {}

    def eval_me(self, inp):
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
        outp = [0]
        for iteration in range(len(inp) - 2):
            outp.append((inp[iteration + 1] - inp[iteration]))
        return outp


class MedianFilter(GeneralNodeFunction):
    """
    Median filter with frame randomly 3 or 5.
    """

    def __init__(self):
        random.seed()
        self.params = {'frame': random.randint(1, 3) * 2 + 1}

    def _middle(self, frame):
        return sorted(frame)[int(self.params['frame'] / 2)]

    def eval_me(self, inp):
        border = int((self.params['frame'] - 1) / 2)
        aux = list(inp) #this is copy of list!
        outp = []
        for it in range(border):
            aux.insert(0, aux[0])
            aux.append(aux[-1])
        for step in range(border, len(aux) - border):
            outp.append(self._middle((aux[(step - border):(step + border+1)])))
        return outp


class EvenNoise(GeneralNodeFunction):
    """
    Addind to the signal random noise in selected frame
    """

    def __init__(self):
        random.seed()
        self.params = {}
        self.params['frame'] = 0

    def eval_me(self, inp):
        self.params['frame'] = (max(inp) - min(inp)) / 2
        aux = list(inp)
        for iter in range(len(aux) - 1):
            aux[iter] += (random.random() - 0.5) * self.params['frame']
        return aux


class MovingAverage(GeneralNodeFunction):
    def __init__(self):
        random.seed()
        self.params = {}
        self.params['window'] = random.randint(1, 3) * 2 + 1

    def _runningMeanFast(self, x, N):
        return np.convolve(x, np.ones((N,)) / N)[(N - 1):]

    def eval_me(self, inp):
        #border = int((self.params['window'] - 1) / 2)
        outp = self._runningMeanFast(inp, self.params['window'])
        return list(outp)
