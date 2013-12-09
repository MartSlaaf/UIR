from module import OwnNeuro
import random
from multiprocessing import Process, Queue
from NodesLibrary import *

subject = OwnNeuro(3, 1, 1000)

input_line = []
output_line = []
input_line.append([])
input_line.append([])
input_line.append([])
output_line.append({'name': 'result_of_sum', 'data': []})
random.seed()
diff = DiscrDiff()
median_5 = MedianFilter()
median_5.params['frame'] = 5
median_3 = MedianFilter()
median_3.params['frame'] = 3
tmp = []
f = open('tech_pool_inflow_impnoised.csv', 'r')
lines = f.readlines()
for line in lines:
    tmp.append(float(line))
f.close()
tmp = median_5.eval_me(tmp)
tmp = median_5.eval_me(tmp)
input_line[0] = tmp

f = open('tech_pool_outflow.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[1].append(float(line))
f.close()
tmp = []
f = open('tech_pool_inflow_impnoised.csv', 'r')
lines = f.readlines()
for line in lines:
    tmp.append(float(line))
f.close()
tmp = median_5.eval_me(tmp)
tmp = median_5.eval_me(tmp)
input_line[2] = tmp
f = open('target_diff.csv', 'r')
lines = f.readlines()
for line in lines:
    output_line[0]['data'].append(float(line))
f.close()


subject.train(input_line, output_line)
a = subject.validate()
print a
