import matplotlib.pyplot as plt
import numpy as np 



### Utils ###

def displayData(data, lineV, lineH, title):
    fig, ax = plt.subplots()
    for key in data:
        ax.plot(data[key], label=key)
    ax.legend(loc='lower right')
    ax.set_title(title)
    for index in lineV:
        plt.axvline(x=index, color='black', linestyle='dotted')
    for height in lineH:
        plt.axhline(y=height, color='black', linestyle='-')
    plt.show()

def derivate(data, dx):
    der = {}
    for key in data:
        x = 0
        der[key] = []
        while x < len(data[key]) - dx:
            der[key].append((data[key][x+dx] - data[key][x]) / dx)
            x = x + dx
    return der



dataFrom = 'ex1_data.dict.npy'
rawData = np.load(dataFrom, allow_pickle=True).item()
lineH = [6600000, ]     # the air pressure at the top of Jungfraujoch is around 660 hPa
displayData(rawData, [], lineH, 'Raw data')



### Task 1.1 ###

# determine the stay in Jungfraujoch (in percentage) by checking the interval in which
# the derivative is "zero" and the air pressure is around 660 hPa
dx = 1000
der = derivate(rawData, dx)

lineV = [95, 300]   # first and last index of the interval for the stay at Jungfraujoch (660 hPa)
lineH = []
displayData(der, lineV, lineH, 'Derivative of the data')
for key in der:
    print('The percentage of time spent in Jungfraujoch is: {0:4.3f} according to the {1} sensor'.format((300-95)*1000/len(rawData[key]), key))
print()



### Task 1.2 ###

# calculate the displacement of the sensors using the one in the chest as reference
# the displacement is calculated by averaging the index displacements at different heights (air pressure values)
# due to the noisy measures it is best to calculate the displacements only where the height changes significantly
# in order not to have displacement due to drift, we decided to calculate the average displament over a small interval
# at the really beginning of the most significant pressure drop
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
    # due to noise the displacement might change a lot in some points
    # to prevent this, as the diplacement between adjacent signals is normally "small", we decided to limit it at 200
    if abs(index['wrist'] - index['chest']) < 200 and abs(index['head'] - index['wrist']) < 200 and abs(index['ankle'] - index['head']) < 200:
        # using the chest signal as a reference
        displacement[0].append(index['wrist'] - index['chest'])
        displacement[1].append(index['head'] - index['chest'])
        displacement[2].append(index['ankle'] - index['chest'])
    # else:
        # print('misleading measure due to noise')
    # uncomment the following block to plot the lines corresponding to the displacements
    # linV = []
    # for key in rawData:
    #     linV.append(index[key])
    # linH = [threshold, ]
    # displayData(rawData, linV, linH, 'Displacement at a given level')

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
displayData(rawData, [300720, 318700], [], 'Interval used to infer the sample rate')
samples = 318700 - 300720
timeRide = 26 * 60

rate = samples / timeRide
print('The sample rate is: {0:4.3f} samples per second'.format(rate))
