__author__ = 'martolod'
from random import randint, seed, random
from OwnMath import sampler
from OwnNeuro import OwnNeuro
from OneTree import OneTree


class OneForest():
    def __init__(self, settings, input_row=None, full_output=None, first_forest=None, second_forest=None, xml=None):
        """
        If we get as input two rows - we starting to generating forest.
        Another way is getting to forests - gaining new forest by crossover this two.
        """
        self._trees = []
        self.result_row = []
        self.power = None
        self._neuro = None
        self.full_output = []
        self.settings = settings
        self.fitness = 0
        if input_row and full_output:
            self._generate(list(input_row), list(full_output))
        elif first_forest and second_forest:
            self._crossover(first_forest, second_forest)
        elif xml:
            self._from_portal(xml)
        else:
            raise Exception('wrong arg"s')

    def _generate(self, input_row, full_output):
        """
        Getting sublist of input row, and starting to generate new trees.
        Creating own network.
        """
        new_power = randint(1, len(input_row))
        own_row = sampler(input_row, new_power)
        self.full_output = full_output
        self.power = len(own_row)
        self.result_row = []
        self._neuro = OwnNeuro(self.settings, self.power, len(self.full_output), len(self.full_output[0]['data']))
        self.fitness = 0
        for top in own_row:
            self._trees.append(OneTree(self.settings, input_element=top))

    def _crossover(self, first_forest, second_forest):
        """
        Crossing over two forests.
        Count of trees in new forest - between two previous forests.
        Getting random count of trees from first forest - others from another.
        """
        pair_power = [first_forest.power, second_forest.power]
        self.power = randint(max(1, min(pair_power)-2), max(pair_power) + 1)
        tempor = first_forest.get_trees() + second_forest.get_trees()
        self._trees = sampler(tempor, self.power, True)
        self.full_output = first_forest.full_output
        self._neuro = OwnNeuro(self.settings, self.power, len(self.full_output), len(self.full_output[0]['data']))

    def get_trees(self):
        """
        Sampling count of random trees.
        """
        return self._trees

    def execute(self):
        """
        Activating evaluation of every tree in forest
        """
        self.result_row = []

        for tree in self._trees:
            self.result_row.append(tree.execute())

    def act_neuro(self):
        """activating neuro education
        """
        self._neuro.train(self.result_row, self.full_output)
        self.fitness = self._neuro.validate()

    def mutate(self, full_input):
        """
        With some little probability fully mutate (regenerating full forest)
        Another way try to mutate every tree in forest.
        """
        seed()
        if random() < self.settings.forest_mutation_probability:
            self._generate(full_input, self.full_output)
        else:
            for tree in self._trees:
                tree.mutate(full_input)

    def store_xml(self):
        forest_xml = ''
        for tree in self._trees:
            forest_xml += tree.store_xml()
        return forest_xml

    def _from_portal(self, xml):
        self.full_output = xml['out']
        self.power = len(xml['trees'])
        self._neuro = OwnNeuro(self.settings, self.power, len(self.full_output), len(self.full_output[0]['data']))
        for iteration in xml['trees']:
            self._trees.append(OneTree(self.settings, xml=iteration))

    def to_portal(self):
        trees = []
        for tree in self._trees:
            trees.append(tree.to_portal())
        return {'out': self.full_output, 'trees': trees}