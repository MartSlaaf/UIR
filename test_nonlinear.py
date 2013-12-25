__author__ = 'Martolod Slaaf'
from calculationModule.Experiment import Experiment, Settings
from calculationModule.OwnMath import stopping_count
probabilities = [0.0016694521863087,
                 0.0033445065874036,
                 0.0050252104398539,
                 0.0067116116207313,
                 0.0084037586596125,
                 0.010101700750871]


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

setting = Settings(forest_mutation_probability=0, tree_mutation_probability=0, population_count=6, stopping_criteria=stopping_count(10))
for prob in probabilities:
    setting.forest_mutation_probability = prob
    setting.tree_mutation_probability = prob
    setting.node_mutation_probability = prob
    setting.filename = 'day_nonlinear_prob' + str(prob)
    experiment = Experiment(input_line, output_line, setting)
    experiment.start_experiments_set(3)