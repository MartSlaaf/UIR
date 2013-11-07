import random


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