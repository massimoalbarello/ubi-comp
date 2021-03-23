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
#   - For reference pressure data:
#   - For pressure and altitude calculations: https://github.com/pvlib/pvlib-python
# ----------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib 

# Load data
data = np.load("ex1_data.dict.npy", allow_pickle=True).item()
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 6), sharex=True)

# Key order: chest , head, wrist, ankle
# Plot raw data
for key in data:
    ax[0].plot(data[key], label=key)
ax[0].legend(loc='lower right')
ax[0].set_title("Raw data")

# Answers to part 1 provided by the TAs
removed_samples = {"chest": 0, "head": 119, "wrist": 56, "ankle": 174}

sampling_rate = 13.7  #Hz

# Synchronize data using answers provided for task 1
synced_data = {}
for key in data:
    synced_data[key] = data[key][removed_samples[key]:]

# Plot Synced data
for key in synced_data:
    ax[1].plot(synced_data[key], label=key)
ax[1].legend(loc='lower right')
ax[1].set_title("Synced data")


## Utils ##

def average_in_time_window(data, start, end):
    average=0
    for key in data:
        average += 0.25*np.average(data[key][start:end])
    return average

## Reference data ##

# Create numpy array to hold the pressure measured by the weather station in Jungfraujoch at 3576 m
# The day in the month of dec 2020 is index+1
reference_pressure = np.array([
    6472000, 6439000, 6400000, 6315000, 6353000, 6357000, 6358000, 6300000,
    6402000, 6407000, 6394000, 6395000, 6478000, 6543000, 6538000, 6555000,
    6589000, 6588000, 6565000, 6565000, 6580000, 6606000, 6583000
])

# Python Dict that contains the pressure data at the 16th of December at the cities that the subject could have passed by 

# key = name , data 1 = altitude[m]
places = { "Eigergletscher": [2320, pvlib.atmosphere.alt2pres(2320)],
            "Kl_Scheidegg": [2061, pvlib.atmosphere.alt2pres(2061)],
            "Wengen     ": [1274, pvlib.atmosphere.alt2pres(1274)],
            "Grindelwald":[ 1034, pvlib.atmosphere.alt2pres(1034)],
            "Lauterbrunnen": [802, pvlib.atmosphere.alt2pres(802)],
            "Stechelberg":[ 910, pvlib.atmosphere.alt2pres(910)],
            "Interlaken": [566,pvlib.atmosphere.alt2pres(556)]
            }

### Task 2.1 ###



# From visual inspection, we find a time window in which the subject is at the observatory (3,572 m)
# and average the pressure data to find the pressure measured at the top on that day. 
time_window=[140000, 200000]

pressure_at_top  = average_in_time_window(synced_data, time_window[0], time_window[1])

# Find nearest neighbour in reference pressure array 
index = (np.abs(reference_pressure[:]-pressure_at_top)).argmin()

print("--------------------------------")
print("Question 2.1 :")
print("--------------------------------")
print(f"Average pressure at observatory: %.2f " % pressure_at_top)
print(f"Nearest reference pressure: %.2f" % reference_pressure[index])
print(f"The subject visited Jungfraujoch on %d december 2020" % (index+1))
print()
### Task 2.2 ###

print("--------------------------------")
print("INFO")
print("--------------------------------")

print("Place \t \t Altitude \t Est. pressure")
for key in places:
    print("{0}:\t {1:.1f}\t\t {2:.2f}" .format(key, places[key][0], 100*places[key][1]))

print()

pressure_at_jfj=average_in_time_window(synced_data, 100000, 120000)
estimated_altitude0= pvlib.atmosphere.pres2alt(pressure_at_top/100.0)
print(f"sanity check 1: real altitude: 3572, predicted altitude: %.2f " % estimated_altitude0)
estimated_altitude00= pvlib.atmosphere.pres2alt(pressure_at_jfj/100.0)
print(f"sanity check 2: real altitude: 3463, predicted altitude: %.2f" % estimated_altitude00)

print()


# start flat 1
t1 = [0,38834]
time1=((t1[1]-t1[0])/13.7)/60 #in minutes
pressure1= average_in_time_window(synced_data, t1[0], t1[1])
estimated_altitude1= pvlib.atmosphere.pres2alt(pressure1/100.0)
print("start flat 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure1, time1, estimated_altitude1))

# start flat 2
t2=[38970, 57760]
time2=((t2[1]-t2[0])/13.7)/60 #in minutes
pressure2= average_in_time_window(synced_data, t2[0], t2[1])
estimated_altitude2= pvlib.atmosphere.pres2alt(pressure2/100.0)
print("start flat2: \t pressure: {0:.3f} \t minutes: {1:.3f}  \t estimated alt:{2:.2f} m".format(pressure2, time2, estimated_altitude2))

# first leg of ascent 
t3=[55761,71996]
time3=((t3[1]-t3[0])/13.7)/60 #in minutes
print("Ascent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time3))

# pause in ascent 
t4=[71996,76562]
time4=((t4[1]-t4[0])/13.7)/60 #in minutes
pressure4 = average_in_time_window(synced_data, t4[0], t4[1])
estimated_altitude4=pvlib.atmosphere.pres2alt(pressure4/100.0)
print("Stop 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure4, time4, estimated_altitude4))

# second leg of ascent 
t5=[76563,95000]
time5=((t5[1]-t5[0])/13.7)/60 #in minutes
print("Ascent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time5))

# first leg of descent
t6=[300605,318580]
time6=((t6[1]-t6[0])/13.7)/60 #in minutes
print("Descent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time6))

# first pause in descent 
t7 = [318580, 324261]
time7=((t7[1]-t7[0])/13.7)/60 #in minutes
pressure7 = average_in_time_window(synced_data, t7[0], t7[1])
estimated_altitude7=pvlib.atmosphere.pres2alt(pressure7/100.0)
print("Stop 2: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m ".format(pressure7, time7, estimated_altitude7))

# seconf leg of descent
t8=[324262,335586]
time8=((t8[1]-t8[0])/13.7)/60 #in minutes
print("Descent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time8))

t9=[335587,341221]
time9=((t9[1]-t9[0])/13.7)/60 #in minutes
pressure9 = average_in_time_window(synced_data, t9[0], t9[1])
estimated_altitude9=pvlib.atmosphere.pres2alt(pressure9/100.0)
print("Stop 3: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure9, time9, estimated_altitude9))


plt.show()