__author__ = 'Martolod Slaaf'
from calculationModule.Experiment import Experiment, Settings
from calculationModule.OwnMath import stopping_count

probabilities = [0.005,
                 0.01,
                 0.015,
                 0.02,
                 0.025,
                 0.03]


def from_csv_column(filename):
    current_file = open('inflowData/' + filename, 'r')
    rows = current_file.readlines()
    current_file.close()
    output_list = []
    for row in rows:
        output_list.append(float(row))
    return output_list


input_line = list()
input_line.append({'name': 'outflow', 'data': from_csv_column('tech_pool_outflow.csv')})
input_line.append({'name': 'inflow_noizd', 'data': from_csv_column('tech_pool_inflow_impnoised.csv')})
input_line.append({'name': 'trash', 'data': from_csv_column('tech_pool_trashdata.csv')})
output_line = list()
output_line.append({'name': 'target', 'data': from_csv_column('target_diff.csv')})

setting = Settings(forest_mutation_probability=0, tree_mutation_probability=0, population_count=6, stopping_criteria=stopping_count(10))
for prob in probabilities:
    setting.forest_mutation_probability = prob
    setting.tree_mutation_probability = prob
    setting.node_mutation_probability = prob
    setting.filename = 'day13_prob' + str(prob)
    experiment = Experiment(input_line, output_line, setting)
    experiment.start_experiments_set(3)