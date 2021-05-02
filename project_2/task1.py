import pickle
import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt

with open("./ex2_recordings/participant_01.pkl", "rb") as f:
    participant_1_data = pickle.load(f)



###### Utils ######

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = fs / 2
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, data)
    return y



###### Task 1.1.1 ######

# construct array of right hand's ECG signal samples for participant 1 watching clip 1
rightHandECG_1 = []
t = []
for sample in participant_1_data["recordings"][1]["ECG"]:
    t.append(sample[0])
    rightHandECG_1.append(sample[1])

# number of samples in our signal
n = len(rightHandECG_1)

# sampling frequency of participant 1 ECG
fsECG_1 = participant_1_data["FS_ECG"]

# time duration of the signal
duration = n / fsECG_1

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

# filtering the signal with a lowpass butterworth filter
cutoff = 1  # how much should we set it ???
y = butter_lowpass_filter(rightHandECG_1, cutoff, fs=fsECG_1, order=2)

# plotting f the original and the filtered signal in the time domain
offset = t[0]
for i in range(len(t)):
    t[i] = round(t[i] - offset)

plt.plot(t, rightHandECG_1, label='original ECG signal')
plt.plot(t, y, label='filtered ECG signal')
plt.legend(loc='lower right')
plt.xlabel('time [ms]')
plt.ylabel('ECG signal')
plt.show()
