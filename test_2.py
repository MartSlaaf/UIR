__author__ = 'martolod'

from module import Experiment
from OwnMath import stopping_count
import random

input_line = []
output_line = []
input_line.append({'name': 'first_of_sum', 'data': []})
input_line.append({'name': 'last_of_sum', 'data': []})
output_line.append({'name': 'result_of_sum', 'data': []})
random.seed()
for i in range(1000):
    input_line[0]['data'].append(random.randint(0, 5))
    input_line[1]['data'].append(random.randint(0, 4))
    output_line[0]['data'].append(input_line[0][i] + input_line[1][i])
experiment = Experiment(input_line, output_line)

experiment.start_experiment(stopping_count(4))
