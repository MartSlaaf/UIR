import random
MAX_FORESTS_IN_COLLECTION = 20
MIN_FORESTS_IN_COLLECTION = 20
FOREST_FULL_MUTATION_PROBABILITY = 0.02
TREE_FULL_MUTATION_PROBABILITY = 0.02
NODE_FULL_MUTATION_PROBABILITY = 0.02
PARTITION_OF_EDUCATION_VERIFICATION_SET = 0.6
MAX_EPOCHS = 100
OUTCASTING_EPOCHS = 10


def sampler(origin, dest_number):
    random.seed()
    result = []
    norm = len(origin) - 1
    for i in range(dest_number):
        result.append(origin[int(random.random()*norm)])
    return result


def stopping_count(count):
    def stopper(state):
        return True if state.count == count else False

    return stopper


def stopping_error(deviation):
    def stopper(state):
        return True if state.deviation <= deviation else False

    return stopper