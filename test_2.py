__author__ = 'martolod'

from module import Experiment
from OwnMath import stopping_count
import random

input_line = []
output_line = []
input_line.append([])
input_line.append([])
output_line.append([])
random.seed()
for i in range(1000):
    input_line[0].append(random.randint(0, 5))
    input_line[1].append(random.randint(0, 4))
    output_line[0].append(input_line[0][i] + input_line[1][i])
experiment = Experiment(input_line, output_line)

experiment.start_experiment(stopping_count(4))
