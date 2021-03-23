#!/usr/bin/env python3
#
# Project: Ubiquitous Computing Project 1
# Task 2
#
# Authors: 
#   - Rayan Armani [rarmani@ethz.ch]
#   - Massimo Albarello [malbarello@ethz.ch]
#
# References:
# ---------------------

import numpy as np
import matplotlib.pyplot as plt

# Load data
data = np.load("ex1_data.dict.npy", allow_pickle=True).item() 
fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(10, 6), sharex=True)

# Key order: chest , head, wrist, ankle
# Plot raw data  
for key in data:
    ax[0].plot(data[key], label=key)
    print(data[key][:5])
ax[0].legend(loc='lower right')
ax[0].set_title("Raw data")

# Answers to part 1 provided by the TAs
removed_samples = { "chest": 0, 
                    "head" : 119,
                    "wrist": 56,
                    "ankle": 174 }

sampling_rate=13.7 #Hz

# Synchronize data using answers provided for task 1
synced_data={}
for key in data:
    synced_data[key]=data[key][removed_samples[key]:]

# Plot Synced data
for key in synced_data:
    ax[1].plot(synced_data[key], label=key)
ax[1].legend(loc='lower right')
ax[1].set_title("Synced data")

### Task 2.1 ###

# Create numpy array to hold the pressure measured by the weather station in Jungfraujoch at m
# The day in the month of dec 2020 is index+1
reference_pressure = np.array([
    6472000, 6439000, 6400000, 6315000, 6353000, 6357000, 6358000, 6300000,
    6402000, 6407000, 6394000, 6395000, 6478000, 6543000, 6538000, 6555000,
    6589000, 6588000, 6565000, 6565000, 6580000, 6606000, 6583000
])

# From visual inspection, we find a time window in which the subject is at the observatory ( m)
# and average the pressure data to find the pressure measured at the top on that day. 
time_window=[140000, 200000]
pressure_at_top = 0

for key in synced_data:
    pressure_at_top += 0.25*np.average(synced_data[key][time_window[0]:time_window[1]])

# find nearest neighbour in reference pressure array 
index = (np.abs(reference_pressure[:]-pressure_at_top)).argmin()

print("-----------")
print("Question 2.1 :")
print("-----------")
print(f"Average pressure at observatory: %.2f " % pressure_at_top)
print(f"Nearest reference pressure: %.2f" % reference_pressure[index])
print(f"The subject visited Jungfraujoch on %d december 2020" % (index+1))

plt.show()