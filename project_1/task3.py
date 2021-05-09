#!/usr/bin/env python3
#
# Project: Ubiquitous Computing Project 1
# Task 2
#
# Authors:
#   - Rayan Armani [rarmani@ethz.ch]
#   - Massimo Albarello [malbarello@ethz.ch]
#
# ----------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Utils 
def moving_average(x, window_size):
    return np.convolve(x, np.ones(window_size), 'valid') / window_size

# Load data
data = np.load("ex1_data.dict.npy", allow_pickle=True).item()

# Load accelerometer data
imu_data = np.load('ex1_data_task3.dict.npy', allow_pickle=True).item()

# Create figures for plots
fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(10, 6), sharex=True)
fig2, bx = plt.subplots(nrows=3, ncols=1, figsize=(10, 6), sharex=True)


# Answers to part 1 provided by the TAs
removed_samples = {"chest": 0, "head": 119, "wrist": 56, "ankle": 174}
pressure_sampling_rate = 13.7  #Hz
# Key order: chest , head, wrist, ankle

# Assumption: 
gravity = - 9.81 # m/s**2

# Synchronize data using answers provided for task 1
synced_data = {}
for key in data:
    synced_data[key] = data[key][removed_samples[key]:]

# Plot Synced data
for key in synced_data:
    ax[0].plot(synced_data[key], label=key)
ax[0].legend(loc='lower right')
ax[0].set_title("Synced data")
    
# Altitude plot using results from task 2
elevation = dict () # Unit: Meters
for key in synced_data :
    elevation[key] = [44307.69*(1-(p/10194000)**(0.190284)) for p in synced_data[key]]
    ax[1].plot(elevation[key], label = key)

# Convert acceleration into sensible units
converted_imu = dict() 
for key in imu_data:
    converted_imu[key]= imu_data[key]*gravity/(2**18) 


### Task 3.1 ###

# Vertical velocity is the first derivative of elevation
derivatives= dict() # Unit: Meters/sample
for key in elevation:
    derivatives[key]= np.gradient(elevation[key])

# Scale the derivative to represent velocity
vertical_velocity = dict() # Unit: Meters/second
for key in derivatives:
    vertical_velocity[key]= derivatives[key]*pressure_sampling_rate
    ax[2].plot(vertical_velocity[key], label = key)
ax[2].set_ylim([-200,200])    
ax[2].legend(loc='lower right')
ax[2].set_title("Vertical velocities [m/s]")

# The maximum speed is defined as the maximum average vertical velocity over a period of 3 seconds.
# So we compute the average of velocity in 3s windows

# number of samples in 3s
n_samples = int(3.0*pressure_sampling_rate)

avg_speed = dict()
for key in derivatives:
    avg_speed[key] = moving_average(vertical_velocity[key],n_samples)
    ax[3].plot(avg_speed[key],label= key)
ax[3].set_ylim([-50,50])    
ax[3].legend(loc='lower right')
ax[3].set_title("Vertical velocities 3s moving average [m/s]")  

# The elevator rides take place in the following time intervals
elevator_up = [134000,134500]
elevator_down = [210200,210750]

# Plot the lines deliminting the sections
ax[1].axvline(x=elevator_up[0], color='black', linestyle='-', label='elevator sections')
ax[1].axvline(x=elevator_up[1], color='black', linestyle='-')
ax[1].axvline(x=elevator_down[0], color='black', linestyle='-')
ax[1].axvline(x=elevator_down[1], color='black', linestyle='-')
ax[1].legend(loc='lower right')
ax[1].set_title("Elevation [m]")

max_speeds_up = []
# Maximum speed of the elevator going up is the maximum of avg_speed in the elevator up interval
for key in avg_speed:
    interval= avg_speed[key][elevator_up[0]:elevator_up[1]]
    vmax = np.amax(interval)
    max_speeds_up.append(vmax)

max_speeds_down = []
# Maximum speed of the elevator going up is the maximum of avg_speed in the elevator up interval
for key in avg_speed:
    interval= avg_speed[key][elevator_down[0]:elevator_down[1]]
    vmax = np.amin(interval)
    max_speeds_down.append(vmax)

# We take the average of the maximum speeds obtained by the signals:
max_speed_up = np.average(max_speeds_up)
max_speed_down = -np.average(max_speeds_down) # we need the absolute value so we take the negative of the down speed


print("--------------------------------")
print("Question 3.1 :")
print("--------------------------------")
print(f"Maximum speed of elevator going up: %.2f m/s" % max_speed_up)
print(f"Maximum speed of elevator going down: %.2f m/s" % max_speed_down)
print()

### Task 3.2 ###

# Under the assumptions that all sensors on a device turn on and off at the same time, then
# the 'Chest' sensor and the IMU are On for the same duration. 

# Total time for which the sensors were on: number of pressure samples / sampling rate
total_time = len(data["chest"])/pressure_sampling_rate # seconds

# Number of IMU samples: all equal so getting one axis is enough
imu_samples = len(imu_data['X'])

imu_sampling_rate = imu_samples/total_time

print("--------------------------------")
print("Question 3.2 :")
print("--------------------------------")
print(f"IMU sampling rate: %.1f Hz" % imu_sampling_rate)
print()

### Task 3.3 ###

# plot chest pressure data wrt time 
x1 = np.arange(len(synced_data['chest']))/pressure_sampling_rate
bx[0].plot(x1,synced_data['chest'], label='chest')
bx[0].legend(loc='lower right')
bx[0].set_title("Pressure data")

x2= np.arange(len(imu_data['X']))/imu_sampling_rate

# plot imu data 
for key in imu_data:
    bx[1].plot(x2,imu_data[key], label=key)
  
# When the subject is walking, the accelerometer signals is expected to have larger amplitude oscillations
# than when he is standing/siting still or in a vehicle.

# We can therefore identify the sections in which the subject is walking by looking at the signal variance 

# Find rolling variance
time_window = int(0.8*imu_sampling_rate)

variance = dict()
for key in imu_data:
    ts = pd.Series(imu_data[key])
    var= ts.rolling(time_window).var()
    #smooth out the variance by takng the rolling mean 
    variance[key] = var.rolling(time_window).mean()
    bx[2].plot(x2,variance[key], label =key)
    

# From the information we know about the itinerary, we can narrow down the areas in which we expect the subject 
# walk from those we expect him not to (ex: car ride from Grindelwald to Zurich), which helps us determine a 
# threshold for the variance

variance_threshold_x= 7.8e8

intervals=[335000, len(imu_data['X'])-100000]
time_intervals= [intervals[0]/imu_sampling_rate, intervals[1]/imu_sampling_rate]
car_ride_time=25140
car_ride_index=int(car_ride_time*imu_sampling_rate)
bx[2].axhline(y=variance_threshold_x, color='black', linestyle='-', label="variance threshold")
bx[2].axvline(x=car_ride_time, color = "grey", linestyle=':', label= "start of car ride")
bx[2].axvline(x=time_intervals[0], color= 'red', linestyle=':', label="beginning of journey")
bx[2].axvline(x=time_intervals[1], color= 'orange', linestyle=':', label= "end of journey")

var = variance['X'].to_numpy()

# Find indices of values greater than threshold (on X trace, because it has the largest variance)
indices = np.asarray(np.nonzero(var>variance_threshold_x)).reshape((-1,1))
bx[2].scatter(indices/imu_sampling_rate, 2e9*(np.ones(len(indices))), marker='x' ,color='black')

# Delimit intervals from indices 
index_gap = int(0.8*imu_sampling_rate)

walking=np.zeros((0,2))


for i in range(len(indices)-1):
    if (indices[i+1]-indices[i])>=index_gap:
        first = indices[i]
        second = indices[i+1]
        section=np.asarray([first, second]).reshape((1,2))
        walking = np.vstack((walking,section))

# Rearrange the values to make start-end values
walking = walking.flatten()
walking = walking[1:(len(walking)-1)]
walking = walking.reshape((-1,2))

# Remove intervals that happen outside the area of interest
pruned_walking=np.zeros((0,2))
for row in walking:
    if row[0]>=intervals[0] and row[1]<=car_ride_index:
        pruned_walking=np.vstack((pruned_walking, row))
walking = pruned_walking

# Plot selected walking intervals
bx[2].scatter(walking[:,0]/imu_sampling_rate, 2e9*(np.ones(len(walking[:,0]))), marker='o' ,color='red', label = "walking interval start")
bx[2].scatter(walking[:,1]/imu_sampling_rate, 2e9*(np.ones(len(walking[:,1]))), marker='o' ,color='orange', label = "walking interval end")

# Add up duration of individual walking intervals 
walking_duration = 0
for row in walking:
    walking_duration = walking_duration + row[1]-row[0]

# Calculate percentage of walking time
walking_percentage = 100.0*(walking_duration/len(imu_data['X']))

# Walking patterns are peridical so we can count the nuber of steps bu counting periodic peaks inside walking intervals
# Count the peaks in the walking intervals
valid_peaks=np.zeros((0,1))
for row in walking:
    peaks,__ = find_peaks(imu_data['X'][int(row[0]):int(row[1])], distance=0.4*imu_sampling_rate, prominence= 20)
    peaks = peaks+row[0]
    valid_peaks=np.append(valid_peaks,peaks)
valid_peaks=valid_peaks.astype(int)

step_count = len(valid_peaks)

bx[1].scatter(valid_peaks/imu_sampling_rate, imu_data['X'][valid_peaks], marker = "x" , color = "red", label= "valid peaks")
bx[1].legend(loc='lower right')
bx[1].set_title("IMU data")

bx[2].legend(loc='lower right')
bx[2].set_title("Rolling variance of IMU data")

print("--------------------------------")
print("Question 3.3:")
print("--------------------------------")
print(f"Percentage of the trip spent walking: %.1f %%" % walking_percentage)
print(f"Number fo steps taken: %d" % step_count)
print()

plt.show()
