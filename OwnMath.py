import random
MAX_FORESTS_IN_COLLECTION = 4
MIN_FORESTS_IN_COLLECTION = 4
FOREST_FULL_MUTATION_PROBABILITY = 0.02
TREE_FULL_MUTATION_PROBABILITY = 0.02
NODE_FULL_MUTATION_PROBABILITY = 0.02
PARTITION_OF_EDUCATION_VERIFICATION_SET = 0.6
MAX_EPOCHS = 10
OUTCASTING_EPOCHS = 2


def sampler(origin, dest_number):
    random.seed()
    result = []
    for i in range(dest_number):
        result.append(origin[int(random.random()*dest_number)])
    return result


def stopping_count(count):
    def stopper(state):
        return True if state.count == count else False

    return stopper


def stopping_error(deviation):
    def stopper(state):
        return True if state.deviation <= deviation else False

    return stopper