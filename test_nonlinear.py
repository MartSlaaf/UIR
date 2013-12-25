__author__ = 'Martolod Slaaf'
from calculationModule.Experiment import Experiment, Settings
from calculationModule.OwnMath import stopping_count

def from_csv_column(filename):
    current_file = open('inflowData/' + filename, 'r')
    rows = current_file.readlines()
    current_file.close()
    output_list = []
    for row in rows:
        output_list.append(float(row))
    return output_list


input_line = list()
input_line.append({'name': 'sum', 'data': from_csv_column('nonlinear_sum.csv')})
input_line.append({'name': 'trash2', 'data': from_csv_column('nonlinear_trash_2.csv')})
input_line.append({'name': 'xor2', 'data': from_csv_column('nonlinear_xor_2.csv')})
input_line.append({'name': 'trash3', 'data': from_csv_column('nonlinear_trash_3.csv')})
input_line.append({'name': 'xor1', 'data': from_csv_column('nonlinear_xor_1.csv')})
input_line.append({'name': 'trash1', 'data': from_csv_column('nonlinear_trash_1.csv')})
output_line = list()
output_line.append({'name': 'target', 'data': from_csv_column('nonlinear_target.csv')})

setting = Settings(population_count=6, stopping_criteria=stopping_count(10), file_string='day15_nonlinearday_')
experiment = Experiment(input_line, output_line)
experiment.start_experiments_set(3)