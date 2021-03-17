import utils
import matplotlib.pyplot as plt
import numpy as np 

dataFrom = 'ex1_data.dict.npy'
rawData = np.load(dataFrom, allow_pickle=True).item()
lineH = [6600000, ]     # the air pressure at the top of Jungfraujoch is around 660 hPa
utils.displayData(rawData, [], lineH)



### Task 1.1 ###

# determine the stay in Jungfraujoch (in percentage) by checking the interval in which
# the derivative is "zero" and the air pressure is around 660 hPa
dx = 1000
der = utils.derivate(rawData, dx)

lineV = [95, 300]   # first and last index of the interval for the stay at Jungfraujoch (660 hPa)
lineH = []
utils.displayData(der, lineV, lineH)
for key in der:
    print('The percentage of time spent in Jungfraujoch is: {0:4.3f} according to the {1} sensor'.format((300-95)*1000/len(rawData[key]), key))
print()



### Task 1.2 ###

# calculate the displacement of the sensors using the one in the chest as reference
# the displacement is calculated by averaging the index displacements at different heights (air pressure values)
# due to the noisy measures it is best to calculate the displacements only where the height changes significantly
thresholds = np.linspace(9000000, 8500000, 100)
index = {}
for key in rawData:
    index[key] = 0
displacement = {}
for i in range(3):
    displacement[i] = []
avg = {}
std = {}
for threshold in thresholds:
    for key in rawData:
        if rawData[key][index[key]] > threshold:
            while rawData[key][index[key]] > threshold:
                index[key] += 1
        else:
            while rawData[key][index[key]] < threshold:
                index[key] += 1
        # print(key, index[key])
    if abs(index['wrist'] - index['chest']) < 200 and abs(index['head'] - index['wrist']) < 200 and abs(index['ankle'] - index['head']) < 200:
        displacement[0].append(index['wrist'] - index['chest'])
        displacement[1].append(index['head'] - index['chest'])
        displacement[2].append(index['ankle'] - index['chest'])
    # else:
        # print('misleading measure')
    # linV = []
    # for key in rawData:
    #     linV.append(index[key])
    # linH = [threshold, ]
    # utils.displayData(rawData, linV, linH)

# for i in range(3):
#     print(displacement[i])

for i in range(3):
    avg[i] = np.mean(displacement[i])
    std[i] = np.std(displacement[i])
    
print('The average displacement between wrist and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[0], std[0]))
print('The average displacement between head and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[1], std[1]))
print('The average displacement between ankle and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[2], std[2]))
print()


### Task 1.3 ###

# calculating the sample rate by dividing the number of samples during the way down from 
# Jungfraujoch to Eigergletscher by the time of the ride (26 minutes)
utils.displayData(rawData, [300720, 318700], [])
samples = 318700 - 300720
timeRide = 26 * 60

rate = samples / timeRide
print('The sample rate is: {0:4.3f} samples per second'.format(rate))