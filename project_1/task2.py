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



plt.show()