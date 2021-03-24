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

# Answers to part 1 provided by the TAs
removed_samples = {"chest": 0, "head": 119, "wrist": 56, "ankle": 174}

sampling_rate = 13.7  #Hz

# Synchronize data using answers provided for task 1
synced_data = {}
for key in data:
    synced_data[key] = data[key][removed_samples[key]:]

# Plot Synced data
for key in synced_data:
    plt.plot(synced_data[key], label=key)
plt.legend(loc='lower right')



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
places = {  "JungfrauJoch": [3463, pvlib.atmosphere.alt2pres(3463)],
            "Top of Europe": [3572, pvlib.atmosphere.alt2pres(3572)],
            "Eigergletscher": [2320, pvlib.atmosphere.alt2pres(2320)],
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
    print("{0}:\t {1:.1f}\t\t {2:.2f}".format(key, places[key][0], 100*places[key][1]))

print()

estimated_altitude = []

# start flat 1
t1 = [0,38834]
time1=((t1[1]-t1[0])/13.7)/60 #in minutes
pressure1= average_in_time_window(synced_data, t1[0], t1[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure1/100.0))
print("start flat 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure1, time1, estimated_altitude[0]))
# expand sample based on the time spent at that altitude
for t in range(round(time1)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure1/100.0))

# start flat 2
t2=[38970, 57760]
time2=((t2[1]-t2[0])/13.7)/60 #in minutes
pressure2= average_in_time_window(synced_data, t2[0], t2[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure2/100.0))
print("start flat2: \t pressure: {0:.3f} \t minutes: {1:.3f}  \t estimated alt:{2:.2f} m".format(pressure2, time2, estimated_altitude[1]))
# expand sample based on the time spent at that altitude
for t in range(round(time2)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure2/100.0))

# first leg of ascent 
t3=[55761,71996]
time3=((t3[1]-t3[0])/13.7)/60 #in minutes
print("Ascent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time3))

# pause in ascent 
t4=[71996,76562]
time4=((t4[1]-t4[0])/13.7)/60 #in minutes
pressure4 = average_in_time_window(synced_data, t4[0], t4[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure4/100.0))
print("Stop 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure4, time4, estimated_altitude[2]))
# expand sample based on the time spent at that altitude
for t in range(round(time4)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure4/100.0))

# second leg of ascent 
t5=[76563,95000]
time5=((t5[1]-t5[0])/13.7)/60 #in minutes
print("Ascent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time5))

# at the top
pressure_at_jfj = average_in_time_window(synced_data, 100000, 120000)
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure_at_jfj/100.0))
print("Jungfraujoch: \t pressure: {0:.3f} \t minutes: ---------- \t estimated alt: {1:.2f} m".format(pressure_at_jfj, estimated_altitude[3]))
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure_at_top/100.0))
print("Top of Europe: \t pressure: {0:.3f} \t minutes: ---------- \t estimated alt: {1:.2f} m".format(pressure_at_top, estimated_altitude[4]))

# first leg of descent
t6=[300605,318580]
time6=((t6[1]-t6[0])/13.7)/60 #in minutes
print("Descent 1: \t pressure: ---------- \t minutes: {0:.3f}".format(time6))

# first pause in descent 
t7 = [318580, 324261]
time7=((t7[1]-t7[0])/13.7)/60 #in minutes
pressure7 = average_in_time_window(synced_data, t7[0], t7[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure7/100.0))
print("Stop 2: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m ".format(pressure7, time7, estimated_altitude[5]))
# expand sample based on the time spent at that altitude
for t in range(round(time7)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure7/100.0))

# seconf leg of descent
t8 = [324262,335586]
time8 = ((t8[1]-t8[0])/13.7)/60 #in minutes
print("Descent 2: \t pressure: ---------- \t minutes: {0:.3f}".format(time8))

t9 = [335587,341221]
time9=((t9[1]-t9[0])/13.7)/60 #in minutes
pressure9 = average_in_time_window(synced_data, t9[0], t9[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure9/100.0))
print("Stop 3: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure9, time9, estimated_altitude[6]))
# expand sample based on the time spent at that altitude
for t in range(round(time9)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure9/100.0))

# noisy interval 1 after stop 3
t10 = [360840,364230]
time10=((t10[1]-t10[0])/13.7)/60 #in minutes
pressure10 = average_in_time_window(synced_data, t10[0], t10[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure10/100.0))
print("Noisy 1: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure10, time10, estimated_altitude[7]))
# expand sample based on the time spent at that altitude
for t in range(round(time10)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure10/100.0))

# noisy interval 2 after stop 3
t11 = [366430,369730]
time11=((t11[1]-t11[0])/13.7)/60 #in minutes
pressure11 = average_in_time_window(synced_data, t11[0], t11[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure11/100.0))
print("Noisy 2: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure11, time11, estimated_altitude[8]))
# expand sample based on the time spent at that altitude
for t in range(round(time11)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure11/100.0))

# noisy interval 3 after stop 3
t12 = [372180,374280]
time12=((t12[1]-t12[0])/13.7)/60 #in minutes
pressure12 = average_in_time_window(synced_data, t12[0], t12[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure12/100.0))
print("Noisy 3: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure12, time12, estimated_altitude[9]))
# expand sample based on the time spent at that altitude
for t in range(round(time12)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure12/100.0))

# tip at index 381126
pressure13 = average_in_time_window(synced_data, 381125, 381127)
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure13/100.0))
print("Tip 1:         \t pressure: {0:.3f} \t minutes: ---------- \t estimated alt:{1:.2f} m".format(pressure13, estimated_altitude[10]))

# noisy interval 4 after stop 3
t14 = [399100,419670]
time14=((t14[1]-t14[0])/13.7)/60 #in minutes
pressure14 = average_in_time_window(synced_data, t14[0], t14[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure14/100.0))
print("Noisy 4: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure14, time14, estimated_altitude[11]))
# expand sample based on the time spent at that altitude
for t in range(round(time14)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure14/100.0))

# tip at index 425930
pressure15 = average_in_time_window(synced_data, 425920, 525940)
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure15/100.0))
print("Tip 2:         \t pressure: {0:.3f} \t minutes: ---------- \t estimated alt:{1:.2f} m".format(pressure15, estimated_altitude[12]))

# noisy interval 5 after stop 3
t16 = [430480,439620]
time16=((t16[1]-t16[0])/13.7)/60 #in minutes
pressure16 = average_in_time_window(synced_data, t16[0], t16[1])
estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure16/100.0))
print("Noisy 5: \t pressure: {0:.3f} \t minutes: {1:.3f} \t estimated alt:{2:.2f} m".format(pressure16, time16, estimated_altitude[13]))
# expand sample based on the time spent at that altitude
for t in range(round(time16)):
    estimated_altitude.append(pvlib.atmosphere.pres2alt(pressure16/100.0))

# Plot altitude data
plt.figure(figsize=(6, 3))
plt.plot(estimated_altitude, label='altitude')
colors = ['black', 'red', 'blue', 'green', 'orange', 'violet', 'aqua', 'grey', 'pink']
for i, place in enumerate(places):
    plt.hlines(y=places[place][0], xmin=0, xmax=len(estimated_altitude), colors=colors[i], linestyles='dotted', label=place)
plt.legend(loc='upper right')

plt.show()