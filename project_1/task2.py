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
places = {  "Jungfraujoch" : [3463, pvlib.atmosphere.alt2pres(3463)],
            "Eigergletscher": [2320, pvlib.atmosphere.alt2pres(2320)],
            "Kl_Scheidegg": [2061, pvlib.atmosphere.alt2pres(2061)],
            "Wengen     ": [1274, pvlib.atmosphere.alt2pres(1274)],
            "Grindelwald":[ 1034, pvlib.atmosphere.alt2pres(1034)],
            "Lauterbrunnen": [802, pvlib.atmosphere.alt2pres(802)],
            "Stechelberg":[ 910, pvlib.atmosphere.alt2pres(910)],
            "Interlaken": [566,pvlib.atmosphere.alt2pres(556)],
            "Luzern    ":[766, pvlib.atmosphere.alt2pres(766)],
            "Zurich    ":[408,pvlib.atmosphere.alt2pres(480)],
            "Basel    ":[256, pvlib.atmosphere.alt2pres(256)],
            "Bern    ": [532,pvlib.atmosphere.alt2pres(532)]           
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

### Tasks 2.2 and 2.3 ###

# From visual inspection we split the curve into sections that correspond to different activities: 
# Flat areas correspond to waiting times between transport(s) or staying at the top
# Slopes correspond to travel time

# Using an open source library we estimate the altitude correspoding to the measured air pressure
# Using the sample time we estimate the length of each time interval

print("--------------------------------")
print("INFO")
print("--------------------------------")

# Reference altitudes of the cities to consider (Wikipedia)
print("Place \t \t Altitude \t Est. pressure")
for key in places:
    print("{0}:\t {1:.1f}\t\t {2:.2f}" .format(key, places[key][0], 100*places[key][1]))

print()

# We check the calculated estimates to known altitudes
pressure_at_jfj=average_in_time_window(synced_data, 100000, 120000)
estimated_altitude0= pvlib.atmosphere.pres2alt(pressure_at_top/100.0)
print(f"sanity check 1: real altitude: 3572, predicted altitude: %.2f " % estimated_altitude0)
estimated_altitude00= pvlib.atmosphere.pres2alt(pressure_at_jfj/100.0)
print(f"sanity check 2: real altitude: 3463, predicted altitude: %.2f" % estimated_altitude00)

# We notice a 50m shift between estimated and actual pressure. This will help us narrow down the locations to consider
# print(3572 - estimated_altitude0)
# print(3463 - estimated_altitude00)


time = [0]
time_cumul=sum(time)

# Segmenting the curve into different activity segments 
# start flat 1
t1 = [0,38834]
time1=((t1[1]-t1[0])/13.7)/60 #in minutes
time.append(time1)
time_cumul=sum(time)
pressure1= average_in_time_window(synced_data, t1[0], t1[1])
estimated_altitude1= pvlib.atmosphere.pres2alt(pressure1/100.0)
estimated_altitude= [estimated_altitude1]
estimated_altitude.append(estimated_altitude1)
print("start flat 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure1, time1, estimated_altitude1))

# start flat 2
t2=[38970, 57760]
time2=((t2[1]-t2[0])/13.7)/60 #in minutes
time.append(time_cumul+time2)
time_cumul += time2

pressure2= average_in_time_window(synced_data, t2[0], t2[1])
estimated_altitude2= pvlib.atmosphere.pres2alt(pressure2/100.0)
estimated_altitude.append(estimated_altitude2)
print("start flat2: \t pressure: {0:.3f} \t minutes: {1:.3f}  \t estimated alt:{2:.2f} m".format(pressure2, time2, estimated_altitude2))

# first leg of ascent 
t3=[55761,71996]
time3=((t3[1]-t3[0])/13.7)/60 #in minutes
time.append(time_cumul+time3)
time_cumul += time3
print("Ascent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time3))

# pause in ascent 
t4=[71996,76562]
time4=((t4[1]-t4[0])/13.7)/60 #in minutes
time.append(time_cumul+time4)
time_cumul += time4

pressure4 = average_in_time_window(synced_data, t4[0], t4[1])
estimated_altitude4=pvlib.atmosphere.pres2alt(pressure4/100.0)
estimated_altitude.append(estimated_altitude4)
estimated_altitude.append(estimated_altitude4)

print("Stop 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure4, time4, estimated_altitude4))

# second leg of ascent 
t5=[76563,95000]
time5=((t5[1]-t5[0])/13.7)/60 #in minutes
time.append(time_cumul+time5)
time_cumul += time5

print("Ascent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time5))
estimated_altitude.append(estimated_altitude00)
# first leg of descent
t6=[300605,318580]
time6=((t6[1]-t6[0])/13.7)/60 #in minutes
time.append(time_cumul+time6)
time_cumul += time6
print("Descent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time6))

# first pause in descent 
t7 = [318580, 324261]
time7=((t7[1]-t7[0])/13.7)/60 #in minutes
time.append(time_cumul+time7)
time_cumul += time7

pressure7 = average_in_time_window(synced_data, t7[0], t7[1])
estimated_altitude7=pvlib.atmosphere.pres2alt(pressure7/100.0)
estimated_altitude.append(estimated_altitude7)
estimated_altitude.append(estimated_altitude7)
print("Stop 2: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m ".format(pressure7, time7, estimated_altitude7))

# seconf leg of descent
t8=[324262,335586]
time8=((t8[1]-t8[0])/13.7)/60 #in minutes
time.append(time_cumul+time8)
time_cumul += time8

print("Descent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time8))

t9=[335587,341221]
time9=((t9[1]-t9[0])/13.7)/60 #in minutes
time.append(time_cumul+time9)
time_cumul += time9
pressure9 = average_in_time_window(synced_data, t9[0], t9[1])
estimated_altitude9=pvlib.atmosphere.pres2alt(pressure9/100.0)
estimated_altitude.append(estimated_altitude9)
estimated_altitude.append(estimated_altitude9)
print("Stop 3: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure9, time9, estimated_altitude9))

t11 = [345400, 381030]
time11= ((t11[1]-t11[0])/13.7)/60 #in minutes
time.append(time_cumul+time11)
time_cumul += time11
estimated_altitude11 = pvlib.atmosphere.pres2alt(9028000/100.0)
estimated_altitude.append(estimated_altitude11)
print("GW to peak:  \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(9028000,time11, estimated_altitude11))

t12 = [381030,446740]
time12= ((t12[1]-t12[0])/13.7)/60 #in minutes
time.append(time_cumul+time12)
time_cumul += time12
print("Peak to end:  \t pressure: ---------- \t minutes: {0:.3f}".format(time12))


t10=[345000,446740]
pressure10 = average_in_time_window(synced_data, t10[1]-5, t10[1])
time10=((t10[1]-t10[0])/13.7)/60 #in minutes
estimated_altitude10=pvlib.atmosphere.pres2alt(pressure10/100.0)
estimated_altitude.append(estimated_altitude10)
print("GW to End: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure10, time10, estimated_altitude10))

estimated_altitude = [x+60 for x in estimated_altitude]
# Plot altitude data
fig1 =plt.figure()
plt.plot(time, estimated_altitude, label="estimated_altitude")
colors= ["red", "orange", "blue", "green", "black", "gray", "aqua", "indigo", "yellow", "pink", "lime", "brown"]
for i, place in enumerate(places):
    plt.hlines(y=places[place][0], xmin=0, xmax=time[-1], color=colors[i], linestyle= "dotted", label=place)
plt.legend(loc='upper right')

print()

print("By comparing durations and altitudes to public transit schedules and Google maps we conclude that:")
print("Starting point: Grindelwald" )
print("starting route: Grindelwald -> Eigergletscher -> Jungfraujoch")
print()
print("Possible passing points")
print("Interlaken: \t True")
print("Zurich: \t True")
print("Luzern: \t True")
print("Grindelwald: \t True")
print("Basel: \t\tFalse")
print("Bern: \t\tFalse")
print("Kleine Scheidegg: False")
print("Lauterbrunnen: \t False")
print("Wengen: \t False")

plt.show()
