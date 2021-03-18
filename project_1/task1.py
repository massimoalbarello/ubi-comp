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
up_there =np.zeros((0,1))
for start, end, average in plateau:
    if average<reference:
        Jungfrau_duration += end - start
        # Show selected segments on the synced plot
        ax[2].plot(start, average, marker='|', markersize= 12, color ='k')
        ax[2].plot(np.arange(start, end), np.ones((int(end-start)))*(average-100000),linestyle="dashed", color = 'k' , label = "At Jungfrau" )
        ax[2].plot(end, average, marker='|', markersize= 12, color ='k')

        up_there=np.vstack((up_there, average))

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

# # Find peaks on the smoothed gradient
# peaks={}
# for key in derivatives: 
#     peaks[key]=  utils.sorted_peaks(derivatives[key])

# # TODO: implement a nearest neighbour peak filtering
# # Temporary way: only fix wrist array
# peaks["wrist"]=peaks["wrist"][2:]

# # Add peaks to smoothed derivative plot
# for key in derivatives: 
#     ax[1].scatter(peaks[key], derivatives[key][peaks[key]], marker ='x')

# wrist_chest=peaks["wrist"]-peaks["chest"]
# head_chest= peaks["head"]- peaks["chest"]
# print(head_chest)
# ankle_chest = peaks["ankle"]- peaks["chest"]

# wirst_shift = int(wrist_chest.mean())
# head_shift = int(head_chest.mean())
# ankle_shift = int(ankle_chest.mean())

# Other method: Take a portion of data at the beginning and compare the number of samples in each log 
# We choose a limit close to the beginning of the trip to minimise the offset from drift
pressue_limit =8500000
x_limit = 200000

ind_chest = np.array(np.where(data["chest"][:x_limit]>pressue_limit)).reshape((-1,1))
ind_ankle = np.array(np.where(data["ankle"][:x_limit]>pressue_limit)).reshape((-1,1))
ind_head = np.array(np.where(data["head"][:x_limit]>pressue_limit)).reshape((-1,1))
ind_wrist = np.array(np.where(data["wrist"][:x_limit]>pressue_limit)).reshape((-1,1))

head_shift = int(ind_head[-1]-ind_chest[-1] )
ankle_shift = int(ind_ankle[-1] -ind_chest[-1]) 
wirst_shift = int(ind_wrist[-1] -ind_chest[-1] )

print("-----------")
print("Question 1.2 : Method 1: Samples removed from the beginning of:")
print("-----------")
print("Wrist sensor:",wirst_shift)
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

# We know the elevator takes 25s to travel 108m (Jungfrau.ch website)
# We also know from observation which peaks in the data correspond to teh elevator rides

# Number of samples corresponding to the elevator rides: 
threshold_down_1= up_there[1,0]
threshold_up = up_there[2,0]
threshold_down_2 = up_there[3,0]

n_samples=[]
# Elevator ride up
idx= np.array(np.where(data["chest"][133750:135000]<= (threshold_down_1-3000))).reshape((-1,1))
idx= idx + 133750 
elevator_start1=idx[0]
ax[2].scatter(idx[0],data["chest"][idx[0]], marker='o')

idx= np.array(np.where(data["chest"][133750:135000] >=(threshold_up+5000))).reshape((-1,1))
idx= idx + 133750 
elevator_end1=idx[-1]
ax[2].scatter(idx[-1],data["chest"][idx[-1]], marker='o')

n_samples = elevator_end1-elevator_start1
sampling = (n_samples/25.0)*0.5
print(n_samples/25.0)

# Elevator ride down
idx= np.array(np.where(data["chest"][210000:211000]<= (threshold_down_2-5000))).reshape((-1,1))
idx= idx + 210000 
elevator_end2=idx[-1]
ax[2].scatter(idx[-1],data["chest"][idx[-1]], marker='o')

idx= np.array(np.where(data["chest"][210000:211000] >=(threshold_up+4200))).reshape((-1,1))
idx= idx + 210000
elevator_start2=idx[0]
ax[2].scatter(idx[0],data["chest"][idx[0]], marker='o')

n_samples= elevator_end2-elevator_start2
print(n_samples/25.0)
sampling += (n_samples/25.0)*0.5

print("-----------")
print("Question 1.3 :")
print("-----------")
print(f"sampling rate is: %.2f Hz" %sampling)



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
plt.show()



