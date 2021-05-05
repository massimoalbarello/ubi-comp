import pickle
import numpy as np
from scipy import signal, fft, stats
import matplotlib.pyplot as plt
import pandas as pd

with open("./ex2_recordings/participant_01.pkl", "rb") as f:
    participant_1_data = pickle.load(f)



###### Utils ######

def butter_filter(data, cutoff, fType, fs, order):
    nyq = fs / 2
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = signal.butter(order, normal_cutoff, btype=fType, analog=False)
    y = signal.filtfilt(b, a, data)
    return y


def statisticalMeasurements(values, name):
    mean = np.mean(values)
    stdev = np.std(values)
    skewness = stats.skew(values)
    kurtosis = stats.kurtosis(values)
    print("\nThe {} values have: \nmean: {:.2f}\nstandard deviation: {:.2f}\nskewness: {:.2f}\nkurtosis: {:.2f}".format(name, mean, stdev, skewness, kurtosis))

    tot = len(values)
    count = 0
    for value in values:
        if value < mean - stdev or value > mean + stdev:
            count += 1
    print('The percentage of times the {} is more than a standard deviation away from the mean is: {:.2f}%'.format(name, count/tot))



###### Task 1.1.1 ######

# construct array of right hand's ECG signal samples for participant 1 watching clip 1
rightHandECG_1 = []
for sample in participant_1_data["recordings"][1]["ECG"]:
    rightHandECG_1.append(sample[1])

# number of samples in our signal
n = len(rightHandECG_1)

# sampling frequency of participant 1 ECG
fsECG_1 = participant_1_data["FS_ECG"]

# time duration of the signal
duration = n / fsECG_1
# print("The duration of the ECG signal is: {} seconds.".format(duration))

# plotting the power specral density for the right hand of the first participant's ECG signal while watching clip 1
f, Pxx_den = signal.welch(rightHandECG_1, fsECG_1)  # any idea on how to set nperseg ???
# considering PSD within 0-40 Hz
f = f[:41]
Pxx_den = Pxx_den[:41]
plt.semilogy(f, Pxx_den)
plt.title('PSD of the ECG signal')
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()



###### Task 1.1.2 ######

# http://ems12lead.com/2014/03/10/understanding-ecg-filtering/

# plotting the FFT of the original signal
fourierTransform = fft.fft(rightHandECG_1)
xf = fft.fftfreq(n, 1/fsECG_1)   # number of sample of the FFT
plt.semilogy(xf, np.abs(fourierTransform))
plt.title('FFT of the ECG signal')
plt.xlabel('frequency [Hz]')
plt.show()

# filtering the signal with a butterworth filter
cutoff = 0.05  # remove DC component
filteredSignal = butter_filter(rightHandECG_1, cutoff, 'high', fs=fsECG_1, order=2)
cutoff = 40     # remove muscle noise component over 40 Hz
filteredSignal = butter_filter(filteredSignal, cutoff, 'low', fs=fsECG_1, order=2)

# plotting f the original and the filtered signal in the time domain
offset = participant_1_data["recordings"][1]["ECG"][0][0]
i = 0
offset_recordings = []
for sample in participant_1_data["recordings"][1]["ECG"]:
    time = round(sample[0] - offset)
    offset_recordings.append([time, filteredSignal[i], sample[2]])
    i += 1

t = []
for sample in offset_recordings:
    t.append(sample[0])

plt.plot(t, rightHandECG_1, label='original ECG signal')
plt.plot(t, filteredSignal, label='filtered ECG signal')
plt.legend(loc='lower right')
plt.xlabel('time [ms]')
plt.ylabel('ECG signal')
plt.show()



###### Task 1.1.4 ######
    
endtime = offset_recordings[-1][0]
time = offset_recordings[0][0]
index = 0   # index of the first sample in the last 50 seconds of the recording
while time < endtime - 50000:    
    index += 1
    time = offset_recordings[index][0]

last50sec = offset_recordings[index:]

# space the samples in the last 50 seconds of the recording so that we can then calculate the inter beat interval in seconds
# in the 'samples' array each index corresponds tp 1 ms
samples = []
i = 0
lastSample = last50sec[i]
for sample in last50sec[1:]:
    inter = 1
    samples.append(sample[1])
    while inter < sample[0] - lastSample[0]:
        samples.append(0)    # fake value used only to extend the array so that two adjacent samples have the real distance in time
        inter += 1
    i += 1
    lastSample = last50sec[i]

peaks, _ = signal.find_peaks(samples, distance=600)
plt.plot(samples)
for i in peaks:
    plt.axvline(i, ymin=0.6, ymax=0.8, color='r')
# plt.plot(peaks, samples[peaks], "x")
plt.show()

interBeatInter = np.diff(peaks)     # time difference in ms between adjacent heart beats
# print(interBeatInter)
statisticalMeasurements(interBeatInter, 'inter beat interval')

heartRateVar = np.diff(interBeatInter)  # time difference in ms between two adjacent inter beat intervals
# print(heartRateVar)
statisticalMeasurements(heartRateVar, 'heart rate variability')

# using moving average to calculate "local" heart rate
window_size = 5     #averaging over 5 inter beat inetervals
numbers_series = pd.Series(1/interBeatInter*1000)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
heartRate= moving_averages_list[window_size - 1:]
# print(heartRate)
statisticalMeasurements(heartRate, 'heart rate')

