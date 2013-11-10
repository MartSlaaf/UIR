from module import OwnNeuro
import random

subject = OwnNeuro(2, 1, 1000)
"""
f = open('tech_pool_outflow.csv', 'r')
lines = f.readlines()
input_line = []
output_line = []
input_line.append([])
input_line.append([])
output_line.append([])
for line in lines:
    input_line[0].append(float(line))
f.close()
f = open('tech_pool_inflow.csv', 'r')
lines = f.readlines()
for line in lines:
    input_line[1].append(float(line))
f.close()
f = open('tech_pool_target.csv', 'r')
lines = f.readlines()
for line in lines:
    output_line[0].append(float(line))
f.close()
"""
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
    print input_line[0][i], input_line[1][i], output_line[0][i]
"""
input_line = [[0, 0, 1, 1], [0, 1, 0, 1]]
output_line = [[0, 1, 1, 0]]
"""
subject.educate(input_line, output_line)
result = subject.validate()
print result

print subject.network.activate([1, 1]), 2
print subject.network.activate([3, 2]), 5
print subject.network.activate([4, 5]), 9