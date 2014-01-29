__author__ = 'martolod'

import xml.etree.ElementTree as ElementTree

LIST_OF_ENTERS = ['inflow_noizd', 'outflow', 'trash']
inputs = ['tfk_recmutation_prob0.00840375865961_experiment' + str(i) + '.xml' for i in xrange(15)]

geners = 15
maximums = [[] for i in range(geners)]
averages = [[] for i in range(geners)]
trashinp = [[] for i in range(geners)]
inflowinp = [[] for i in range(geners)]
outflowinp = [[] for i in range(geners)]
dd = [[] for i in range(geners)]
nofilter = [[] for i in range(geners)]
evennoise = [[] for i in range(geners)]
outflowinp = [[] for i in range(geners)]
median = [[] for i in range(geners)]
average = [[] for i in range(geners)]
powers = [[] for i in range(geners)]

for iter_input in inputs:
    tree = ElementTree.parse('../outflowData/' + iter_input)
    root = tree.getroot()
    i = 0
    for generation in root:
        localTrash = 0
        localIflow = 0
        localOutflow = 0
        fitnesses = []
        local_powers = []
        localAvg = 0
        localMed = 0
        localNo = 0
        localNoise = 0
        localDD = 0
        for forest in generation:
            fitnesses.append(float(forest.attrib['fitness']))
            local_powers.append(int(forest.attrib['power']))
            for tree in forest:
                if tree.attrib['input'] == 'trash':
                    localTrash += 1
                if tree.attrib['input'] == 'inflow_noizd':
                    localIflow += 1
                    for node in tree:
                        if node.attrib['function'] == 'MedianFilter':
                            localMed += 1
                        elif node.attrib['function'] == 'MovingAverage':
                            localAvg += 1
                        elif node.attrib['function'] == 'NoFilter':
                            localNo += 1
                        elif node.attrib['function'] == 'DiscrDiff':
                            localDD += 1
                        elif node.attrib['function'] == 'EvenNoise':
                            localNoise += 1
                if tree.attrib['input'] == 'outflow':
                    localOutflow += 1
        average[i].append(localAvg)
        median[i].append(localMed)
        trashinp[i].append(localTrash)
        inflowinp[i].append(localIflow)
        outflowinp[i].append(localOutflow)
        dd[i].append(localDD)
        nofilter[i].append(localNo)
        evennoise[i].append(localNoise)
        powers[i].append(sum(local_powers)/len(local_powers))
        maximums[i].append(max(fitnesses))
        averages[i].append(sum(fitnesses) / len(fitnesses))
        i += 1

outfile = open('result.csv', 'w')
outfile.writelines('max_max;min_max;avg_max;max_avg;min_avg;avg_avg;trashdata;inflow;outflow;MovingAverage;Median;nofilter;discrdiff;evennoise;powers;' + '\n')
for i in range(geners):
    outline = str(max(maximums[i])) + ';' + str(min(maximums[i])) + ';' + str(
        sum(maximums[i]) / len(maximums[i])) + ';' + str(max(averages[i])) + ';' + str(min(averages[i])) + ';' + str(
        sum(averages[i]) / len(averages[i])) + ';' + str(float(sum(trashinp[i])) / len(trashinp[i])) + ';' + str(float(sum(inflowinp[i])) / len(inflowinp[i])) + ';' + str(float(sum(outflowinp[i])) / len(outflowinp[i])) + ';' + str(
        float(sum(average[i])) / len(average[i])) + ';' + str(float(sum(median[i])) / len(median[i])) + ';' + str(float(sum(nofilter[i])) / len(nofilter[i])) + ';' + str(float(sum(dd[i])) / len(dd[i])) + ';' + str(float(sum(evennoise[i])) / len(evennoise[i])) + ';' + str(float(sum(powers[i])) / len(powers[i])) + ';'
    outfile.writelines(outline + '\n')
outfile.close()
