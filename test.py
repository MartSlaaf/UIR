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
for i in range(1000):
    input_line[0].append(random.randint(0, 5))
    input_line[1].append(random.randint(0, 4))
    output_line[0]['data'].append(input_line[0][i] + input_line[1][i])
mainfuckingquie = Queue()


def analizator(a, q):
    q.put(a)


q = 1
p = 100
a = Process(target=analizator, args=(q, mainfuckingquie))
b = Process(target=analizator, args=(p, mainfuckingquie))
a.start()
b.start()
a.join()
b.join()
print mainfuckingquie.qsize(), mainfuckingquie.get(), mainfuckingquie.get()

"""
a = Process(target=subject.educate, args=(list(input_line), list(output_line),))
b = Process(target=dabject.educate, args=(list(input_line), list(output_line),))
a.start()
b.start()
a.join()
b.join()


print subject.validate()
print dabject.validate()
"""