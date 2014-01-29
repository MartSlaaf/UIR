__author__ = 'martolod'

import xml.etree.ElementTree as ElementTree

LIST_OF_ENTERS = ['inflow_noizd', 'outflow', 'trash']
inputs = ['tfk_fm_nonlinear_prob0.01_experiment' + str(i) + '.xml' for i in xrange(10)]

geners = 10
maximums = [[] for i in range(geners)]
averages = [[] for i in range(geners)]
trashinp1 = [[] for i in range(geners)]
trashinp2 = [[] for i in range(geners)]
trashinp3 = [[] for i in range(geners)]
xor1 = [[] for i in range(geners)]
xor2 = [[] for i in range(geners)]
sumvhod = [[] for i in range(geners)]
dd1 = [[] for i in range(geners)]
nofilter1 = [[] for i in range(geners)]
evennoise1 = [[] for i in range(geners)]
median1 = [[] for i in range(geners)]
average1 = [[] for i in range(geners)]
powers = [[] for i in range(geners)]
dd2 = [[] for i in range(geners)]
nofilter2 = [[] for i in range(geners)]
evennoise2 = [[] for i in range(geners)]
median2 = [[] for i in range(geners)]
average2 = [[] for i in range(geners)]

for iter_input in inputs:
    tree = ElementTree.parse('../outflowData/' + iter_input)
    root = tree.getroot()
    i = 0
    for generation in root:
        localTrash1 = 0
        localTrash2 = 0
        localTrash3 = 0
        localxor1 = 0
        localxor2 = 0
        localsuminp = 0
        fitnesses = []
        local_powers = []
        localAvg1 = 0
        localMed1 = 0
        localNo1= 0
        localNoise1 = 0
        localDD1 = 0
        localAvg2 = 0
        localMed2 = 0
        localNo2= 0
        localNoise2 = 0
        localDD2 = 0
        for forest in generation:
            fitnesses.append(float(forest.attrib['fitness']))
            local_powers.append(int(forest.attrib['power']))
            for tree in forest:
                if tree.attrib['input'] == 'trash1':
                    localTrash1 += 1
                if tree.attrib['input'] == 'trash2':
                    localTrash2 += 1
                if tree.attrib['input'] == 'trash3':
                    localTrash3 += 1
                if tree.attrib['input'] == 'sum':
                    localsuminp += 1
                if tree.attrib['input'] == 'xor1':
                    localxor1 += 1
                    for node in tree:
                        if node.attrib['function'] == 'MedianFilter':
                            localMed1 += 1
                        elif node.attrib['function'] == 'MovingAverage':
                            localAvg1 += 1
                        elif node.attrib['function'] == 'NoFilter':
                            localNo1 += 1
                        elif node.attrib['function'] == 'DiscrDiff':
                            localDD1 += 1
                        elif node.attrib['function'] == 'EvenNoise':
                            localNoise1 += 1
                if tree.attrib['input'] == 'xor2':
                    localxor2 += 1
                    for node in tree:
                        if node.attrib['function'] == 'MedianFilter':
                            localMed2 += 1
                        elif node.attrib['function'] == 'MovingAverage':
                            localAvg2 += 1
                        elif node.attrib['function'] == 'NoFilter':
                            localNo2 += 1
                        elif node.attrib['function'] == 'DiscrDiff':
                            localDD2 += 1
                        elif node.attrib['function'] == 'EvenNoise':
                            localNoise2 += 1
        trashinp1[i].append(localTrash1)
        trashinp2[i].append(localTrash2)
        trashinp3[i].append(localTrash3)
        sumvhod[i].append(localsuminp)
        xor1[i].append(localxor1)
        xor2[i].append(localxor2)
        
        dd1[i].append(localDD1)
        nofilter1[i].append(localNo1)
        evennoise1[i].append(localNoise1)
        median1[i].append(localMed1)
        average1[i].append(localAvg1)
        
        dd2[i].append(localDD2)
        nofilter2[i].append(localNo2)
        evennoise2[i].append(localNoise2)
        median2[i].append(localMed2)
        average2[i].append(localAvg2)
        
        powers[i].append(sum(local_powers)/len(local_powers))
        maximums[i].append(max(fitnesses))
        averages[i].append(sum(fitnesses) / len(fitnesses))
        i += 1

outfile = open('result.csv', 'w')
outfile.writelines('max_max;min_max;avg_max;max_avg;min_avg;avg_avg;trash1;trash2;trash3;xor1;xor2;sum;MovingAverage_xor1;Median_xor1;nofilter_xor1;discrdiff_xor1;evennoise_xor1;MovingAverage_xor2;Median_xor2;nofilter_xor2;discrdiff_xor2;evennoise_xor2;powers;' + '\n')
for i in range(geners):
    outline = str(max(maximums[i])) + ';' + str(min(maximums[i])) + ';' + str(sum(maximums[i]) / len(maximums[i])) + ';' + str(max(averages[i])) + ';' + str(min(averages[i])) + ';' + str(sum(averages[i]) / len(averages[i])) + ';' + str(float(sum(trashinp1[i])) / len(trashinp1[i])) + ';' + str(float(sum(trashinp2[i])) / len(trashinp2[i])) + ';' + str(float(sum(trashinp3[i])) / len(trashinp3[i])) + ';' + str(float(sum(xor1[i])) / len(xor1[i])) + ';' + str(float(sum(xor2[i])) / len(xor2[i])) + ';' + str(float(sum(sumvhod[i])) / len(sumvhod[i])) + ';' + str(float(sum(average1[i])) / len(average1[i])) + ';' + str(float(sum(median1[i])) / len(median1[i])) + ';' + str(float(sum(nofilter1[i])) / len(nofilter1[i])) + ';' + str(float(sum(dd1[i])) / len(dd1[i])) + ';' + str(float(sum(evennoise2[i])) / len(evennoise2[i])) + ';' + str(float(sum(average2[i])) / len(average2[i])) + ';' + str(float(sum(median2[i])) / len(median2[i])) + ';' + str(float(sum(nofilter2[i])) / len(nofilter2[i])) + ';' + str(float(sum(dd2[i])) / len(dd2[i])) + ';' + str(float(sum(evennoise2[i])) / len(evennoise2[i])) + ';' + str(float(sum(powers[i])) / len(powers[i])) + ';' 
    outfile.writelines(outline + '\n')
outfile.close()
