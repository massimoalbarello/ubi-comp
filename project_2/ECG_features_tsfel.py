import tsfel
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

with open("ex2_recordings/participant_01.pkl", "rb") as f:
    particiapnt_01_data = pickle.load(f)

# Low pass filter definition functions
def butter_bandpass(lowcut, highcut,fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order,[low,high], btype='bandpass')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    y = signal.filtfilt(b, a, data)
    return y

def find_features(signal, fs, name):
    # print(signal)
    features = tsfel.time_series_features_extractor(cfg_file, signal, fs=fs, window_size=len(signal))    # Receives a time series sampled at 256 Hz, divides into windows of size 1280 (i.e. 5 seconds) and extracts all features
    print('Statistical measurements of: {}'.format(name))
    for feature in features:
        print('{}: {}'.format(feature, features[feature][0]))
    # plt.plot(filtered_lead1_ecg_p1)
    # plt.show()
    return features

# Low pass filter implementation
# Parameters
lowcut = 4 #[Hz]
highcut = 20
ECG_freq = particiapnt_01_data["FS_ECG"]
fs = ECG_freq

raw_ECG_p1 = np.array(particiapnt_01_data["recordings"][1]["ECG"])
lead1_ecg_p1= np.array(raw_ECG_p1[:,1]-raw_ECG_p1[:,2])
t = np.array(raw_ECG_p1[:,0]) - raw_ECG_p1[0,0] #[ms]


# Choose filter order
order = 2
# Apply the low pass filer to the lead I ECG filter
filtered_lead1_ecg_p1 = butter_bandpass_filter(lead1_ecg_p1,lowcut, highcut, fs, order)

# print(filtered_lead1_ecg_p1)

# Truncate the signal to look at only the last 50s of the signal
filtered_lead1_ecg_50s = filtered_lead1_ecg_p1[-(50*fs):] 
t = t[-(50*fs):]
t = t - t[0]

peaks, _ = signal.find_peaks(filtered_lead1_ecg_50s, distance=150)
# plt.plot(filtered_lead1_ecg_50s)
# for i in peaks:
#     plt.axvline(i, ymin=0.6, ymax=0.8, color='r')
# # plt.plot(peaks, samples[peaks], "x")
# plt.show()

# print('\nCLIP {} of participant {}'.format(clip, i))
interBeatInter = np.diff(peaks/fs)     # time difference in ms between adjacent heart beats
# print(interBeatInter)
interBeatInterval = pd.DataFrame(interBeatInter)

cfg_file = tsfel.get_features_by_domain("statistical")      # If no argument is passed retrieves all available features
# print(cfg_file["statistical"].keys())

for feature in cfg_file["temporal"].keys():
    if feature != 'Mean'  and feature != 'Skewness' and feature != 'Standard deviation' and feature != 'Kurtosis':
        cfg_file["statistical"][feature]["use"] = 'no'
    else:
        cfg_file["statistical"][feature]["use"] = 'yes'
    # print('{}: {}'.format(feature, cfg_file["statistical"][feature]["use"]))

# print(interBeatInterval)
features = find_features(interBeatInterval, fs, 'interbeat interval')

heartRateVar = np.diff(interBeatInter)  # time difference in ms between two adjacent inter beat intervals
features = find_features(heartRateVar, fs, 'heart rate variability')

# using moving average to calculate "local" heart rate
window_size = 5     #averaging over 5 inter beat inetervals
numbers_series = pd.Series(1/interBeatInter)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
heartRate = moving_averages_list[window_size - 1:]
features = find_features(heartRate, fs, 'heart rate')





