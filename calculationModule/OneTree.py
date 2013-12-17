__author__ = 'martolod'
from NodesLibrary import *
from OwnMath import sampler


class OneTree():
    """Class of one tree in modification forest trees
    """

    def _generate(self, input_element):
        """
        Generating one tree. Getting one input element as root.
        Creating chain of random functions.
        """
        nodes = sampler(LIST_OF_FUNCTIONS, random.randint(1, len(LIST_OF_FUNCTIONS)))
        self._nodes = []
        for node in nodes:
            self._nodes.append(eval(node)())
        self._inputElement = input_element

    def __init__(self, settings, input_element=None, xml=None):
        self._nodes = []
        self._inputElement = {}
        self.settings = settings
        if input_element:
            self._generate(input_element)
        elif xml:
            self._from_portal(xml)
        else:
            raise Exception('wrong arg"s')

    def execute(self):
        """
        Chain calculate results of every function in tree, starting from root value.
        """
        preput = self._inputElement['data']
        for node in self._nodes:
            preput = node.eval_me(preput)
        return preput

    def mutate(self, input_raw):
        """
        With some little probability mutate whole tree - regenerate it.
        Other way is try to mutate every node. Mutating node is just regenerating it.
        """
        random.seed()
        if random.random() < self.settings.tree_mutation_probability:
            self._generate(input_raw[random.randint(0, len(input_raw)-1)])
        else:
            for nodenumber in range(len(self._nodes)):
                if random.random() < self.settings.node_mutation_probability:
                    self._nodes[nodenumber] = eval(LIST_OF_FUNCTIONS[random.randint(0, len(LIST_OF_FUNCTIONS) - 1)])()

    def store_xml(self):
        current_tree = '<tree input="' + str(self._inputElement['name']) + '" power="' + str(len(self._nodes)) + '">\n'
        for node in self._nodes:
            current_tree += node.store_xml()
        current_tree += '</tree>\n'
        return current_tree

    def _from_portal(self, xml):
        self._inputElement = xml['input']
        for noder in xml['nodes']:
            self._nodes.append(eval(noder['name'])())
            self._nodes[-1].params = noder['params']

    def to_portal(self):
        noder = []
        for node in self._nodes:
            noder.append({'name': node.__class__.__name__, 'params': node.params})
        return {'input': self._inputElement, 'nodes': noder}