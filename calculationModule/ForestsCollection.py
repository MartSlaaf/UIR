__author__ = 'martolod'
from OneForest import OneForest
from multiprocessing import Process, Queue
from copy import copy
from random import random


def main_async_method(queue, xml, a, settings):
    forest = OneForest(settings, xml=xml)
    forest.execute()
    forest.act_neuro()
    queue.put({'fitness': forest.fitness, 'place': a})
    print '| | |-finished ', queue.qsize(), ' forest. fitness =', forest.fitness


class ForestCollection():
    def __init__(self, settings, input_row=None, output_row=None, previous_generation=None):
        """
        If passed two rows - start generating collection of forests.
        Other way, if passed previous generation of collection - spawning next generation
        """
        self._fullInput = []
        self.power = 0
        self._forests = []
        self._fullOutput = []
        self.best_fitness = 0
        self.roulet = []
        self.settings = settings
        if input_row and output_row:
            self._generate(list(input_row), list(output_row))
        elif previous_generation:
            self._next_generation(previous_generation)
        else:
            raise Exception('wrong arg"s')

    def _generate(self, input_row, output_row):
        """
        Generating number of forests (it's random in some frame).
        """
        self._fullInput = input_row
        self.power = self.settings.population_count
        self._fullOutput = output_row
        for one_forest in range(self.power):
            self._forests.append(OneForest(self.settings, input_row=self._fullInput, full_output=self._fullOutput))

    def _next_generation(self, previous_generation):
        """
        Spawning next generation of collection by selecting n pairs of distinct forests from previous generation
        and them over.
        """
        self._fullInput, self._fullOutput = previous_generation.get_data()
        self.power = self.settings.population_count
        for forest_iteration in range(self.power):
            first, second = previous_generation.selection()
            print 'selected for crossover ->', first.fitness, second.fitness
            self._forests.append(OneForest(self.settings, first_forest=first, second_forest=second))

    def get_data(self):
        """
        Just outputting private data.
        """
        return self._fullInput, self._fullOutput

    def execute(self):
        """
        Executing every forest in collection, activating their networks.
        By the way collecting data about best fitness function.
        """
        process_list = []
        forests_queue = Queue(self.power)
        iterational = 0
        print '| |-starting evaluation, training and validation'
        for one_forest in self._forests:
            process_list.append(
                Process(target=main_async_method,
                        args=(forests_queue, copy(one_forest.to_portal()), iterational, self.settings)))
            iterational += 1
        for proc in process_list:
            proc.start()
        for proc in process_list:
            proc.join()
        for smth in range(forests_queue.qsize()):
            tmp = forests_queue.get()
            self._forests[tmp['place']].fitness = tmp['fitness']
        fitness_summ = sum(map(lambda forest: forest.fitness, self._forests))
        fss = map(lambda x: x.fitness, self._forests)
        print 'avg = ', str(sum(fss) / len(fss)), 'max = ', max(fss)
        self.roulet = map(lambda x: x.fitness / fitness_summ, self._forests)

    def select_by_prob(self):
        """selecting one point in probability gist
        """
        ball = random()
        stop_sector = 0
        for sector in self.roulet:
            ball -= sector
            if ball < 0:
                return stop_sector
            else:
                stop_sector += 1
        return stop_sector

    def selection(self):
        """
        Selecting distinct pair of forests for crossover.
        Probability of selecting one forest is as much as that fitness function is better.
        """
        first = self.select_by_prob()
        second = first
        while self._forests[first] == self._forests[second]:
            second = self.select_by_prob()
        return self._forests[first], self._forests[second]

    def mutate(self):
        """
        Just mutating every forest in collection.
        """
        for forest in self._forests:
            forest.mutate(self._fullInput)

    def store_xml(self):
        forests_xml = ''
        for forest in self._forests:
            forests_xml += '<forest power="' + str(forest.power) + '"  fitness="' + str(forest.fitness) + '">\n'
            forests_xml += forest.store_xml()
            forests_xml += '</forest>\n'
        return forests_xml