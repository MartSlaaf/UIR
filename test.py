from module import OwnNeuro
import random
from multiprocessing import Process, Queue

subject = OwnNeuro(2, 1, 1000)
dabject = OwnNeuro(2, 1, 1000)

input_line = []
output_line = []
input_line.append([])
input_line.append([])
output_line.append({'name': 'result_of_sum', 'data': []})
random.seed()
f = open('tech_pool_outflow.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[0].append(float(line))
f.close()
f = open('tech_pool_inflow_impnoised.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[1].append(float(line))
f.close()
f = open('tech_pool_target.csv', 'r')
lines = f.readlines()
for line in lines:
    output_line[0]['data'].append(float(line))
f.close()


subject.educate(input_line, output_line)
print subject.validate()
