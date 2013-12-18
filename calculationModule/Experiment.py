from ForestsCollection import ForestCollection
from OwnMath import stopping_count
from datetime import datetime


class Settings():
    """
    settings class for experiment.
    with some default values
    """

    def __init__(self, forest_mutation_probability=0.02, tree_mutation_probability=0.02, node_mutation_probability=0.02,
                 training_part_fraction=0.75, maximum_training_epochs=100, quit_epochs=10,
                 population_count=12, stopping_criteria=stopping_count(15),
                 file_string=datetime.now().strftime("%Y_%m_%d-%H_%M_%S")):
        self.forest_mutation_probability = forest_mutation_probability
        self.tree_mutation_probability = tree_mutation_probability
        self.node_mutation_probability = node_mutation_probability
        self.training_part_fraction = training_part_fraction
        self.maximum_training_epochs = maximum_training_epochs
        self.quit_epochs = quit_epochs
        self.population_count = population_count
        self.filename = file_string
        self.local_filename = file_string
        #next is function also
        self.stopping_criteria = stopping_criteria


class Experiment():
    def __init__(self, input_row, output_row, settings=Settings()):
        """getting initial data and making initial collection.
        """
        self._fullInput = input_row
        self._fullOutput = output_row
        self.count = 0
        self.fitness = 0
        self.init_collection = ForestCollection(settings, self._fullInput, self._fullOutput)
        self.settings = settings
        self._xml_store = '<?xml version="1.1" encoding="UTF-8" ?>\n<experiment>\n'

    def start_experiment(self):
        """
        Just experiments. While stopping criteria is not actual executing experiment,
        storing results to xml spawning new generation (selecting, crossing, mutating) and so on.
        """
        experimental_collection = self.init_collection
        while not (self.settings.stopping_criteria(self)):
            print 'generation = ', self.count
            print '|-act'
            experimental_collection.execute()

            self.fitness = experimental_collection.best_fitness
            self.count += 1
            self._xml_store += '<iteration generation="' + str(
                self.count) + '">\n'
            self._xml_store += experimental_collection.store_xml()
            self._xml_store += '</iteration>\n'
            print '|-spawn'
            experimental_collection = ForestCollection(self.settings, previous_generation=experimental_collection)
            print '|- mutate'
            experimental_collection.mutate()
        self._xml_store += '</experiment>'
        outc = open(self.settings.local_filename + '.xml', 'w')
        outc.write(self._xml_store)
        outc.close()

    def start_experiments_set(self, count):
        for once in range(count):
            print '-+=>', once, '<=+-'
            self.settings.local_filename = 'outflowData/' + self.settings.filename + '_experiment' + str(once)
            self.start_experiment()
            self.__init__(self._fullInput, self._fullOutput, self.settings)  # reinit for next experiment