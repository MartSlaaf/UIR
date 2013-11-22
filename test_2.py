__author__ = 'martolod'

from module import Experiment
from OwnMath import stopping_count
import random

f = open('tech_pool_outflow.csv', 'r')
lines = f.readlines()
input_line = []
output_line = []
input_line.append({'name': 'inflow', 'data': []})
input_line.append({'name': 'outflow', 'data': []})
output_line.append({'name': 'target', 'data': []})
for line in lines:
    input_line[0]['data'].append(float(line))
f.close()
f = open('tech_pool_inflow_impnoised.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[1]['data'].append(float(line))
f.close()
f = open('tech_pool_target.csv', 'r')
lines = f.readlines()
for line in lines:
    output_line[0]['data'].append(float(line))
f.close()

experiment = Experiment(input_line, output_line)

experiment.start_experiment(stopping_count(4))
