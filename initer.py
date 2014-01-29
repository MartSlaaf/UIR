__author__ = 'Martolod Slaaf'
from calculationModule.Experiment import Experiment, Settings
from calculationModule.OwnMath import stopping_count
from calculationModule.OneForest import OneForest

def from_csv_column(filename):
    current_file = open('inflowData/' + filename, 'r')
    rows = current_file.readlines()
    current_file.close()
    output_list = []
    for row in rows:
        output_list.append(float(row))
    return output_list

setting = Settings(forest_mutation_probability=0, tree_mutation_probability=0, population_count=6, stopping_criteria=stopping_count(10))

forestxmlideal = {'out': [{'name': 'target', 'data': from_csv_column('nonlinear_target.csv')}], 'trees': [{'input':{'name': 'xor1', 'data': from_csv_column('nonlinear_xor_1.csv')}, 'nodes':[{'name': 'MovingAverage', 'params': {'window': 7}}, {'name': 'MedianFilter', 'params': {'frame': 3}}, {'name': 'NoFilter', 'params': {}}]}, {'input': {'name': 'xor2', 'data': from_csv_column('nonlinear_xor_2.csv')}, 'nodes':[{'name': 'NoFilter', 'params': {}}, {'name': 'EvenNoise', 'params': {'frame': 0}}, {'name': 'MovingAverage', 'params': {'window': 5}}, {'name': 'DiscrDiff', 'params': {}}, {'name': 'MedianFilter', 'params': {'frame': 7}}]}, {'input':{'name': 'xor2', 'data': from_csv_column('nonlinear_xor_2.csv')}, 'nodes':[{'name': 'NoFilter', 'params': {}}]}, {'input':{'name': 'sum', 'data': from_csv_column('nonlinear_sum.csv')}, 'nodes':[{'name': 'NoFilter', 'params': {}}]}, {'input':{'name': 'xor2', 'data': from_csv_column('nonlinear_xor_2.csv')}, 'nodes':[{'name': 'NoFilter', 'params': {}}]}]} 
ourforest = OneForest(settings=setting, xml=forestxmlideal)
ourforest.execute()
ourforest.act_neuro()

