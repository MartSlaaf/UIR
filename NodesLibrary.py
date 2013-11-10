import random
import xml.etree.ElementTree as ElementTree

#this is list of classes in strange state.
LIST_OF_FUNCTIONS = ['NodeFunction', 'StrangeFunction', 'VariousFunction']


class GeneralNodeFunction():
    def __init__(self):
        self.params = {'frame': 10, 'crime': 12}

    def eval_me(self, inp):
        outp = inp * self.params['frame'] / self.params['crime']
        return outp

    def store_xml(self, parent):
        ElementTree.SubElement(parent, self.__class__.__name__, attrib=self.params)


class StrangeFunction(GeneralNodeFunction):
    def __init__(self):
        self.params = {'frame': random.randint(0, 10), 'crime': random.randint(1, 11)}

    def eval_me(self, inp):
        outp = inp * 2 * self.params['frame'] / self.params['crime']
        return outp


class VariousFunction():
    def __init__(self):
        self._firstParam = random.randint(-100, 100)
        self._secondParam = random.randint(1, 10)

    def evalMe(self, inp):
        outp = inp * self._firstParam / (self._secondParam * 3.1415926)
        return outp
