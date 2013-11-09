from NodesLibrary import *
from OwnMath import *
import random
from math import log, fabs
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


class OwnNeuro():
    def __init__(self, input_power, output_power, education_power):
        self.input_power = input_power
        self.output_power = output_power
        self.education_power = education_power
        self.training_errors = []
        self.validation_errors = []
        self.data_set = SupervisedDataSet(self.input_power, self.output_power)
        self.hidden_power = int(
            (output_power * education_power / (1 + log(education_power, 2))) / (input_power + output_power)) + 2
        self.network = buildNetwork(self.input_power, self.hidden_power, self.output_power)

    def _form_set(self, input_row, output_row):
        for one_portion in range(self.education_power):
            input_tuple = ()
            for one_input in range(self.input_power):
                input_tuple += (input_row[one_input][one_portion],)
            output_tuple = ()
            for one_output in range(self.output_power):
                output_tuple += (output_row[one_output][one_portion],)
            self.data_set.addSample(input_tuple, output_tuple)

    def educate(self, input_row, output_row):
        self._form_set(input_row, output_row)
        trainer = BackpropTrainer(self.network, self.data_set)
        self.training_errors, self.validation_errors = trainer.trainUntilConvergence(
            validationProportion=PARTITION_OF_EDUCATION_VERIFICATION_SET,
            maxEpochs=MAX_EPOCHS,
            continueEpochs=OUTCASTING_EPOCHS)

    def validate(self):
        print self.validation_errors



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
            else:
                raise Exception('wrong arg"s')

        def execute(self):
            preput = self._inputElement
            for node in self._nodes:
                preput = node.evalMe(preput)
            return preput

        def mutate(self, input_raw):
            random.seed()
            if random.random() < TREE_FULL_MUTATION_PROBABILITY:
                self._generate(input_raw)
            else:
                for nodenumber in range(len(self._nodes)):
                    if random.random() < NODE_FULL_MUTATION_PROBABILITY:
                        self._nodes[nodenumber] = eval(LIST_OF_FUNCTIONS[random.randint(1, len(LIST_OF_FUNCTIONS))])()


    class OneForest():
        def __init__(self, input_row=None, full_output=None, first_forest=None, second_forest=None):
            self._trees = []
            self.result_row = []
            self.power = None
            self._neuro = None
            self.full_output = []
            self.fitness = 0
            if input_row and full_output:
                self._generate(input_row, full_output)
            elif first_forest and second_forest:
                self._crossover(first_forest, second_forest)
            else:
                raise Exception('wrong arg"s')

        def _generate(self, input_row, full_output):
            """
        selecting count of trees.
        """
            own_row = sampler(input_row, random.randint(1, full_output))
            self.full_output = full_output
            self.power = len(own_row)
            self.result_row = []
            self._neuro = OwnNeuro(self.power, len(self.full_output))
            self.fitness = 0
            for top in own_row:
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
            self.full_output = first_forest.full_output
            self._neuro = OwnNeuro(self.power, len(self.full_output))

        def get_trees(self, count):
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
            self._neuro.educate(self.result_row, self.full_output)
            self.fitness = self._neuro.validate(self.result_row, self.full_output)

        def mutate(self, full_input):
            random.seed()
            if random.random() < FOREST_FULL_MUTATION_PROBABILITY:
                self._generate(full_input, self.full_output)
            else:
                for tree in self._trees:
                    tree.mutate(full_input)


    class ForestCollection():
        def __init__(self, input_row=None, output_row=None, previous_generation=None):
            """Selecting number of forests
        """
            self._fullInput = []
            self.power = 0
            self._forests = []
            self._fullOutput = []
            self.best_fitness = 0
            if input_row and output_row:
                self._generate(input_row, output_row)
            elif previous_generation:
                self._next_generation(previous_generation)
            else:
                raise Exception('wrong arg"s')

        def _generate(self, input_row, output_row):
            self._fullInput = input_row
            self.power = random.randint(MIN_FORESTS_IN_COLLECTION, MAX_FORESTS_IN_COLLECTION)
            self._fullOutput = output_row
            for one_forest in range(len(self.power)):
                new_row = sampler(self._fullInput, random.randint(1, self._fullOutput))
                self._forests.append(OneForest(input_row=new_row, full_output=self._fullOutput))

        def _next_generation(self, previous_generation):
            self._fullInput, self._fullOutput = previous_generation.getData()
            self.power = previous_generation.power
            for forest_iteration in range(self.power):
                first, second = self._selection()
                self._forests.append(OneForest(first_forest=first, second_forest=second))

        def getData(self):
            return self._fullInput, self._fullOutput

        def execute(self):
            """
        executing one point of algo
        """
            for one_forest in self._forests:
                one_forest.execute()
                one_forest.act_neuro()
                if one_forest.deviation < self.best_fitness:
                    self.best_fitness = one_forest.deviation

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

        def mutate(self):
            for forest in self._forests:
                forest.mutate()


    class Experiment():
        def __init__(self, input_row, output_row):
            """getting initial data and making initial collection
        """
            self._fullInput = input_row
            self._fullOutput = output_row
            self.count = 0
            self.fitness = 0
            self.init_collection = ForestCollection(self._fullInput, self._fullOutput)

        def start_experiment(self, stopping_criteria):
            experimental_collection = self.init_collection
            while stopping_criteria(self):
                experimental_collection.execute()
                self.fitness = experimental_collection.best_fitness
                self.count += 1
                experimental_collection = ForestCollection(previous_generation=experimental_collection)
                experimental_collection.mutate()
