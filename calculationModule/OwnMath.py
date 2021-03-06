import random


def sampler(origin, dest_number, distinct=False):
    random.seed()
    result = []
    norm = len(origin) - 1
    outresource = []
    if distinct and dest_number < (norm + 2):
        for i in range(dest_number):
            a = int(random.random()*(len(origin)) - 1 + 0.5)
            outresource.append(a)
            result.append(origin.pop(a))
        print '>sampler distinct selecting ' + str(dest_number) + ' from ' + str(norm + 1) + ' = ' + str(outresource)
        return result
    for i in range(dest_number):
        a = int(random.random()*norm + 0.5)
        outresource.append(a)
        result.append(origin[a])
    print '>sampler selecting ' + str(dest_number) + ' from ' + str(len(origin)) + ' = ' + str(outresource)
    return result


def stopping_count(count):
    def stopper(state):
        return True if state.count == count else False

    return stopper


def stopping_error(deviation):
    def stopper(state):
        return True if state.deviation <= deviation else False

    return stopper