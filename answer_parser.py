__author__ = 'martolod'

import xml.etree.ElementTree as ElementTree
from NodesLibrary import LIST_OF_FUNCTIONS
LIST_OF_ENTERS = ['inflow_noizd', 'outflow', 'trash']

tree = ElementTree.parse('outcast.xml')
root = tree.getroot()
stringlist = ['generation;average_fitness;max_fitness;']
for enter in LIST_OF_ENTERS:
    for function in LIST_OF_FUNCTIONS:
        stringlist[-1] += function + '__FOR__' + enter + ';'
for generation in root:
    stringlist.append(generation.attrib['generation'] + ';')
    fitnesses = []
    functions = {x: 0 for x in LIST_OF_FUNCTIONS}
    enters = {x: functions for x in LIST_OF_ENTERS}
    print enters
    for forest in generation:
        fitnesses.append(float(forest.attrib['fitness']))
        for tree in forest:
            for node in tree:
                enters[tree.attrib['input']][node.attrib['function']] += 1
    stringlist[-1] += str(sum(fitnesses)/len(fitnesses)) + ';'
    stringlist[-1] += str(max(fitnesses)) + ';'
    for enter in LIST_OF_ENTERS:
        for function in LIST_OF_FUNCTIONS:
            stringlist[-1] += str(enters[enter][function]) + ';'


outfile = open('result.csv', 'w')
for line in stringlist:
    outfile.writelines(line + '\n')
outfile.close()
