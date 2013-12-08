from module import OwnNeuro
import random
from multiprocessing import Process, Queue

def test():
    subject = OwnNeuro(2, 1, 1000)

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
    f = open('target_diff.csv', 'r')
    lines = f.readlines()
    for line in lines:
        output_line[0]['data'].append(float(line))
    f.close()


    subject.train(input_line, output_line)
    a = subject.validate()

    dabject = OwnNeuro(3, 1, 1000)
    input_line = []
    output_line = []
    input_line.append([])
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
    f = open('tech_pool_trashdata.csv', 'r')
    lines = f.readlines()
    for line in lines:
        input_line[2].append(float(line))
    f.close()
    f = open('target_diff.csv', 'r')
    lines = f.readlines()
    for line in lines:
        output_line[0]['data'].append(float(line))
    f.close()


    dabject.train(input_line, output_line)
    return a, dabject.validate()

first = 0
second = 0
for i in range(120):
    print i
    a, b = test()
    if a >= b:
        first += 1
    else:
        second += 1
print first, second