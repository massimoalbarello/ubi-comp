#!/usr/bin/env python3
#
# Project: Ubiquitous Computing Exercise 1
#
# Authors: 
#   - Rayan Armani [rarmani@ethz.ch]
#     
#
# References:
# ---------------------

import numpy as np
import matplotlib.pyplot as plt
import utils

# First derivative smoothing parameters
cutoff = 1000
fs = 300000

# Data fmeasured at 3571 m
reference_pressure=np.genfromtxt('jungfraujoch_pressure.csv',
                           dtype=float,
                           delimiter=',',
                           skip_header=1)

# Load data
# .item() is needed as np.load() returns a structured array that needs
# to be converted back to a dict. File should be in same location as code.
data = np.load("ex1_data.dict.npy", allow_pickle=True).item() 

fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(10, 6), sharex=True)

for key in data:
    ax[0].plot(data[key], label=key)
ax[0].legend(loc='lower right')
ax[0].set_title("Raw data")

# Compute and plot smoothed gradient
derivatives={}
for key in data:
    derivatives[key]= utils.butter_lowpass_filter(np.gradient(data[key]), cutoff, fs)
    ax[1].plot(derivatives[key], label = key)
ax[1].set_ylim([-1000, 1000])
ax[1].set_title("Smoothed first derivative")
ax[1].legend(loc='lower right')

##################################################
##                QUESTION 1.1                  ##
##################################################

# Define 100% as the length of the shortest sensor data log
log_length = {}
data_keys = data.keys()

for key in data_keys:
    log_length[key]= len(data[key])

shortest_log, total_duration =  min(log_length.items())

# Find plateaux on the smoothed gradient
# Plateau array: start peak, end peak, average pressure 
points , plateau = utils.find_plateaux(data[shortest_log], derivatives[shortest_log])

# Choose threshold from plateau: highest value of air pressure measured in the time interval
# The air pressure is measured at 3571m but the tourist area is at 3,463 m 
# so we need to add a buffer to account for these 100m.
# From the data the difference between the lowest plateau and the other ones is ~100000

reference = np.amax(reference_pressure[:,1]) + 100000.0
Jungfrau_duration = 0 

for start, end, average in plateau:
    if average<reference:
        Jungfrau_duration += end - start
        # Show selected segments on the synced plot
        ax[2].plot(start, average, marker='|', markersize= 12, color ='k')
        ax[2].plot(np.arange(start, end), np.ones((int(end-start)))*(average-100000),linestyle="dashed", color = 'k' , label = "At Jungfrau" )
        ax[2].plot(end, average, marker='|', markersize= 12, color ='k')

time_up_there= 100.0 * Jungfrau_duration/total_duration

# Print Answer to 
print("-----------")
print("Question 1.1:")
print("-----------")
print("Shortest sensor log:", shortest_log)
print("Total duration:", total_duration)
print("Duration at Jungfrau:", int(Jungfrau_duration))
print(f"Portion of trip spent in Jungfrau: %.2f %%" % time_up_there )

##################################################
##                QUESTION 1.2                  ##
##################################################

# Find peaks on the smoothed gradient
peaks={}
for key in derivatives: 
    peaks[key]=  utils.sorted_peaks(derivatives[key])

# TODO: implement a nearest neighbour peak filtering
# Temporary way: only fix wrist array
peaks["wrist"]=peaks["wrist"][2:]

# Add peaks to smoothed derivative plot
for key in derivatives: 
    ax[1].scatter(peaks[key], derivatives[key][peaks[key]], marker ='x')

wrist_chest=peaks["wrist"]-peaks["chest"]
head_chest= peaks["head"]- peaks["chest"]
ankle_chest = peaks["ankle"]- peaks["chest"]

wirst_shift = int(wrist_chest.mean())
head_shift = int(head_chest.mean())
ankle_shift = int(ankle_chest.mean())

# Print Answer to 1.2
print("-----------")
print("Question 1.2 : Samples removed from the beginning of:")
print("-----------")
print("Wirst sensor:",wirst_shift)
print("Head sensor:", head_shift)
print("Ankle sensor:", ankle_shift)

# Adjust the sensor data with respect to chest sensor 
temp_ankle=data["ankle"][ankle_shift:]
temp_head=data["head"][head_shift:]
temp_wrist=data["wrist"][wirst_shift:]

# Plot Adjusted data
ax[2].plot(data["chest"], label="chest")
ax[2].plot(temp_head, label="head")
ax[2].plot(temp_wrist, label="wirst")
ax[2].plot(temp_ankle, label="ankle")
ax[2].legend(loc='lower right')
ax[2].set_title("Synced data")

##################################################
##                QUESTION 1.3                  ##
##################################################

print("-----------")
print("Question 1.3 :")
print("-----------")

##################################################
##                QUESTION 2.1                  ##
##################################################

# The pressure at the Observatory is the closest to the pressure measured by official authorities
# In our case it is the average of the the lowest plateau across all sensors
pressure_at_observatory =0
for key in data:
    points , plateau = utils.find_plateaux(data[key], derivatives[key])
    pressure_at_observatory += np.amin(plateau[:,2])/4.0

# find nearest neighbour in reference array 
index = (np.abs(reference_pressure[:,1]-pressure_at_observatory)).argmin()

print("-----------")
print("Question 2.1 :")
print("-----------")
print(f"Average pressure at observatory: %.2f " % pressure_at_observatory)
print(f"Nearest reference pressure: %.2f" %  reference_pressure[index,1] )
print(f"The subject visited Jungfraujoch on %d december" %reference_pressure[index,0])

plt.savefig('plot.png')
# plt.tight_layout()
# plt.show()



