__author__ = 'martolod'
from math import log, fabs
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import RPropMinusTrainer


class OwnNeuro():
    def __init__(self, settings, input_power, output_power, education_power):
        """
        Creating network base on input parameters: count of inputs, count of outputs and
        count of data tuple in training set.
        Count of neurons in hidden layer calculated by formula, extracted from
        Arnold - Kolmogorov - Hecht-Nielsen theorem in minimalistic form.
        """
        self.input_power = input_power
        self.output_power = output_power
        self.education_power = education_power
        self.training_errors = []
        self.validation_errors = []
        self.data_set = SupervisedDataSet(self.input_power, self.output_power)
        self.inputs_for_validation = []
        self.settings = settings
        self.mse = 0
        self.hidden_power = int(
            (output_power * education_power / (1 + log(education_power, 2))) / (input_power + output_power))
        self.network = buildNetwork(self.input_power, self.hidden_power, self.output_power)

    def _form_set(self, input_row, output_row):
        """
        Method for creating proper training set from given data.
        """
        for one_portion in range(self.education_power):
            input_tuple = ()
            for one_input in range(self.input_power):
                input_tuple += (input_row[one_input][one_portion],)
            self.inputs_for_validation.append(input_tuple)
            output_tuple = ()
            for one_output in range(self.output_power):
                output_tuple += (output_row[one_output]['data'][one_portion],)
            self.data_set.addSample(input_tuple, output_tuple)

    def train(self, input_row, output_row):
        """
        Training network by r-prop.
        PARTITION_OF_EDUCATION_VERIFICATION_SET - education|validation ratio
        MAX_EPOCHS - count of max steps of education
        OUTCASTING_EPOCHS - if education can't get out of local minimum it given count of steps, it stops
        """
        self._form_set(input_row, output_row)
        trainer = RPropMinusTrainer(module=self.network, dataset=self.data_set)
        self.training_errors, self.validation_errors = trainer.trainUntilConvergence(
            validationProportion=self.settings.training_part_fraction,
            maxEpochs=self.settings.maximum_training_epochs,
            continueEpochs=self.settings.quit_epochs)
        len_validate = int(len(output_row[0]['data']) * (1 - self.settings.training_part_fraction))
        results_of = [list(self.network.activate(x))[0] for x in self.inputs_for_validation[len_validate:]]
        self.mse = sum(map(lambda result, target: fabs(result - target), list(results_of),
                           list(output_row[0]['data'][len_validate:]))) / len(results_of)
        print '| | |-MSE = ', self.mse

    def validate(self):
        return 1 / (1 + self.mse)