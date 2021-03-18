#!/usr/bin/env python3
#
# Project: Ubiquitous Computing Project 1
# 
# Authors: 
#   - Rayan Armani [rarmani@ethz.ch]
#   - Massimo Albarello [malbarello@ethz.ch]
#     
#
# References:
# ---------------------


import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz, find_peaks


### Parameters ###

# Filtering
cutoff = 1000
fs = 300000



### Utils ###

def add_lines(fig, lineV, lineH, label):

    for index in lineV:
        fig.axvline(x=index, color='black', linestyle='dotted', label=label)
    for height in lineH:
        fig.axhline(y=height, color='black', linestyle='-', label=label)

# Smoothing  and low pass filering 
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def find_plateaux(signal,derivative):
    '''
    finds flat reagions between signal peaks
    '''
    threshold = 1000
    height= [10,600]
    distance = 100
    prominence = 80
   
    peaks = np.zeros((0,1))
    positive_peaks, __ = find_peaks(derivative,height= height, distance=distance, prominence= prominence)
    negative_peaks, __ = find_peaks(-derivative,height= height, distance = distance, prominence= prominence)
    peaks=np.append(positive_peaks,negative_peaks)
    peaks=np.sort(peaks)
    
    start=0
    end=0
    average=0
    
    plateau=np.zeros((0,3))
    for i in range(len(peaks)-1):
        if peaks[i+1]-peaks[i] > threshold:
            start = peaks[i]
            end = peaks[i+1]
            average=np.average(signal[peaks[i]:peaks[i+1]])

            plateau= np.vstack((plateau,[start, end, average]))
    return plateau

data = np.load("ex1_data.dict.npy", allow_pickle=True).item() 
fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(10, 6), sharex=True)

for key in data:
    ax[0].plot(data[key], label=key)
ax[0].legend(loc='lower right')
ax[0].set_title("Raw data")

### Task 1.1 ###

#  Find the shortest sensor log and its number of samples, to represent the total length of the day trip
log_length = {}
data_keys = data.keys()

for key in data_keys:
    log_length[key]= len(data[key])

shortest_log, total_duration =  min(log_length.items())

# Compute and smooth the first derivative of the signals
derivatives={}
for key in data:
    derivatives[key]= butter_lowpass_filter(np.gradient(data[key]), cutoff, fs)

# Find plateaux (prolonged stay at the same altitude) on the smoothed gradient
# Plateau array: start peak, end peak, average pressure 
plateau = find_plateaux(data[shortest_log], derivatives[shortest_log])

# Find a reasonable threshold below which we can assume the visitor is in Jungfraujoch: 

# We pick the highest air pressure measured between 01.12.2020 and 23.12.2020: 660.6 hPa
# The air pressure is measured at 3571m but the tourist area is at 3,463 m: we expect the 
# tourist pressure to have an air pressure ~ 10 hPa higher

reference = 6606000.0 + 100000.0

Jungfrau_duration = 0 
up_there =np.zeros((0,1))
for start, end, average in plateau:
    if average<reference:
        Jungfrau_duration += end - start

        # Show selected segments on the synced plot
        ax[1].plot(start, average, marker='|', markersize= 12, color ='k')
        ax[1].plot(np.arange(start, end), np.ones((int(end-start)))*(average-100000),linestyle="dashed", color = 'k' , label = "At Jungfrau" )
        ax[1].plot(end, average, marker='|', markersize= 12, color ='k')

time_up_there= 100.0 * Jungfrau_duration/total_duration

# Print Answer 
print("TASK 1 - RESULTS")
print("-----------")
print("Question 1:")
print("-----------")
print("Shortest sensor log:", shortest_log)
print("Total duration:", total_duration)
print("Duration at Jungfraujoch:", int(Jungfrau_duration))
print()
print(f"Portion of trip spent in Jungfraujoch: %.1f %%" % time_up_there )
print()

### Task 1.2 ###

# From visual observation, the chest sensors is the one turned on last
# calculate the displacement of the sensors using the one in the chest as reference
# the displacement is calculated by averaging the index displacements at different heights (air pressure values)
# due to the noisy measures it is best to calculate the displacements only where the height changes significantly
# in order not to have displacement due to drift, we decided to calculate the average displament over a small interval
# at the beginning of the most significant pressure drop

thresholds = np.linspace(9000000, 8500000, 100)
index = {}
for key in data:
    index[key] = 0
displacement = {}
for i in range(3):
    displacement[i] = []
avg = {}
std = {}
for threshold in thresholds:
    for key in data:
        if data[key][index[key]] > threshold:
            while data[key][index[key]] > threshold:
                index[key] += 1
        else:
            while data[key][index[key]] < threshold:
                index[key] += 1

    # due to noise the displacement might change a lot in some points
    # to prevent this, as the diplacement between adjacent signals is normally "small", we decided to limit it at 200
    if abs(index['wrist'] - index['chest']) < 200 and abs(index['head'] - index['wrist']) < 200 and abs(index['ankle'] - index['head']) < 200:
        # using the chest signal as a reference
        displacement[0].append(index['wrist'] - index['chest'])
        displacement[1].append(index['head'] - index['chest'])
        displacement[2].append(index['ankle'] - index['chest'])

for i in range(3):
    avg[i] = np.mean(displacement[i])
    std[i] = np.std(displacement[i])

# Print Answer  
print("-----------")
print("Question 2:")
print("-----------")

print('The average displacement between:')
print('wrist and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[0], std[0]))
print('head and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[1], std[1]))
print('ankle and chest measurements is: {0:4.3f} with a standard deviation of: {1:4.3f}'.format(avg[2], std[2]))
print()

print("Points removed from:")
print(f"Wrist signal: %d" %avg[0])
print(f"Head signal: %d" %avg[1])
print(f"Ankle signal: %d" %avg[2])
print("Chest signal: 0")
print()



# Adjust the sensor data with respect to chest sensor 
temp_wrist=data["wrist"][int(avg[0]):]
temp_head=data["head"][int(avg[1]):]
temp_ankle=data["ankle"][int(avg[2]):]

# Plot Adjusted data
ax[1].plot(data["chest"], label="chest")
ax[1].plot(temp_head, label="head")
ax[1].plot(temp_wrist, label="wirst")
ax[1].plot(temp_ankle, label="ankle")
ax[1].legend(loc='lower right')
ax[1].set_title("Synced data")

### Task 1.3 ###

# We find the number of samples in intervals we know the diration of
# We choose the bounds of these intervals based on visual inspection
# And average the rates calculated from these intervals to get the sample rate


# # Jungfraujoch to Eigergletscher: (26 minutes) - source: SBB schedule
# add_lines(ax[1], [300720, 318700, 134097,134412, 210316, 210657], [])
# samples = 318700 - 300720
# timeRide = 26 * 60
# rate[0,0] = samples / timeRide


add_lines(ax[1], [134097,134412, 210316, 210657], [], "Intervals for sample rate")
ax[1].legend(loc='lower right')
# Elevator ride up (25s) - source Jungfrau.ch website
samples = 134412 - 134097
timeRide = 25
rate1= samples / timeRide


# Elevator ride down (25s)
samples = 210657 - 210316
timeRide = 25
rate2 = samples / timeRide

avg_rate = (rate1+rate2)/2

# Print Answer  
print("-----------")
print("Question 3:")
print("-----------")

print("Rates obtained by visual inspection: {:.2f} , {:.2f}".format(rate1,rate2))
print()
print(f'The sample rate is: %.2f Hz'% avg_rate)
print()


plt.show()
