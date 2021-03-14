#!/usr/bin/env python3
#
# Project: Ubiquitous Computing Exercise 1
# 
#
# Authors: 
#   - Rayan Armani [rarmani@ethz.ch]
#     
#
# References:
# ---------------------

import numpy as np
from scipy.signal import butter, lfilter, freqz, find_peaks


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
 

def sorted_peaks(signal):
    
    # Peak finding parameters
    height= [220,600]
    distance = 100
    prominence = 100
   
    peaks = np.zeros((0,1))
    positive_peaks, __ = find_peaks(signal,height= height, distance=distance, prominence= prominence)
    negative_peaks, __ = find_peaks(-signal,height= height, distance = distance, prominence= prominence)
    peaks=np.append(positive_peaks,negative_peaks)
    peaks=np.sort(peaks)

    return peaks

def find_plateaux(signal,derivative):
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
    return peaks, plateau

    
