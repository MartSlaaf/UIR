__author__ = 'martolod'

from module import Experiment
from OwnMath import stopping_count
from NodesLibrary import DiscrDiff
import random


input_line = []
output_line = []
input_line.append({'name': 'outflow', 'data': []})
input_line.append({'name': 'inflow_noizd', 'data': []})
input_line.append({'name': 'trash', 'data': []})
output_line.append({'name': 'target', 'data': []})
f = open('tech_pool_outflow.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[0]['data'].append(float(line))
f.close()
f = open('tech_pool_inflow_impnoised.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[1]['data'].append(float(line))
f.close()
f = open('tech_pool_trashdata.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[2]['data'].append(float(line))
f.close()
f = open('target_diff.csv', 'r')
lines = f.readlines()
for line in lines:
    output_line[0]['data'].append(float(line))

f.close()
for iteration in range(80):
    print '-+=>', iteration, '<=+-'
    experiment = Experiment(input_line, output_line, '../day7_' + str(iteration) + '.xml')
    experiment.start_experiment(stopping_count(15))

