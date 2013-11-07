from NodesLibrary import *
from OwnMath import *
from sys import maxint as maximum_deviation
import random

MAX_FORESTS_IN_COLLECTION = 15
MIN_FORESTS_IN_COLLECTION = 5


class OneTree():
    """Class of one tree in modification forest trees
    """

    def _generate(self, input_element):
        #get random sample of available nodes
        nodes = sampler(LIST_OF_FUNCTIONS, random.randint(1, len(LIST_OF_FUNCTIONS)))
        #initialize all of
        for node in nodes:
            self._nodes.append(eval(node)())
            #input value
        self._inputElement = input_element

    def __init__(self, input_element=None):
        self._nodes = []
        self._inputElement = 0
        if input_element:
            self._generate(input_element)


class OneForest():
    def __init__(self, input_row=None, full_output=None, first_forest=None, second_forest=None):
        self._trees = []
        self.result_row = []
        self.power = None
        self._neuro = None
        self._fullOutput = []
        self.fitness = maximum_deviation
        if input_row and full_output:
            self._generate(input_row, full_output)
        elif first_forest and second_forest:
            self._crossover(first_forest, second_forest)

    def _generate(self, input_row, full_output):
        """
        selecting count of trees.
        """
        self._fullOutput = full_output
        self.power = len(input_row)
        self._neuro = OwnNeuro(len(input_row), len(self._fullOutput))
        for top in input_row:
            self._trees.append(OneTree(input_element=top))

    def _crossover(self, first_forest, second_forest):
        """crossing over two forests
        """
        self.power = random.randint(first_forest.power, second_forest.power)
        count_first = random.randint(0, self.power)
        for tree in first_forest.get_trees(count_first):
            self._trees.append(tree)
        for tree in second_forest.get_trees(self.power - count_first):
            self._trees.append(tree)



    def get_trees(count):
        return sampler(self._trees, count)

    def execute(self):
        """evaluate all calculations
        """
        self.result_row = []
        for tree in self._trees:
            self.result_row.append(tree.execute())

    def act_neuro(self):
        """activating neuro education
        """
        self._neuro.educate(self.result_row, self._fullOutput)
        self.fitness = self._neuro.validate(self.result_row, self._fullOutput)


    class ForestCollection():
        def __init__(self, input_row, output_row):
            """Selecting number of forests
            """
            self._fullInput = input_row
            self.forests_count = random.randint(MIN_FORESTS_IN_COLLECTION, MAX_FORESTS_IN_COLLECTION)
            self._forests = []
            self._fullOutput = output_row
            self.best_deviation = maximum_deviation
            for one_forest in range(len(self.forests_count)):
                new_row = sampler(self._fullInput, random.randint(1, self._fullOutput))
                self._forests.append(OneForest(new_row, self._fullOutput))

        def execute(self):
            """
            executing one point of algo
            """
            for one_forest in self._forests:
                one_forest.execute()
                one_forest.act_neuro()
                if one_forest.deviation < self.best_deviation:
                    self.best_deviation = one_forest.deviation

        def _selection(self):
            """
            selecting pair of forests for crossover
            """

            def select_by_prob(probability_gist):
                """selecting one point in probability gist
                """
                a = random.random()
                step = 0
                while (step < len(probability_gist)) and (probability_gist[step] < a):
                    step += 1
                return step

            fitness_summ = 0
            for one_forest in self._forests:
                fitness_summ += one_forest.fitness
            probability_gist = []
            temp_probability = 0
            for one_forest in self._forests:
                probability_gist.append(temp_probability + one_forest.fitness / fitness_summ)

            first = select_by_prob(probability_gist)
            second = first
            while second == first:
                second = select_by_prob(probability_gist)

            return self._forests[first], self._forests[second]

        def next_generation(self):
            """Get next generation
            """
            out_generation = []
            for forest_iteration in range(self.forests_count):
                out_generation.append(OneForest.crossover(self._selection()))


    class Experiment():
        def __init__(self, input_row, output_row):
            """getting initial data and making initial collection
            """
            self._fullInput = input_row
            self._fullOutput = output_row
            self.count = 0
            self.deviation = maximum_deviation
            self.init_collection = ForestCollection(self._fullInput, self._fullOutput)

        def start_experiment(self, stopping_criteria):
            experimental_collection = self.init_collection
            while stopping_criteria(self):
                experimental_collection.execute()
                self.deviation = experimental_collection.best_deviation
                self.count += 1
                experimental_collection = experimental_collection.next_generation()
                experimental_collection.mutate()
