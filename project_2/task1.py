import pickle
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

with open("./ex2_recordings/participant_01.pkl", "rb") as f:
    participant_1_data = pickle.load(f)



### Task 1.1 ###

# construct array of right hand's ECG signal samples for participant 1 watching clip 1
rightHandECG_1 = []
for sample in participant_1_data["recordings"][1]["ECG"]:
    rightHandECG_1.append(sample[1])

# sampling frequency of participant 1 ECG
fsECG_1 = participant_1_data["FS_ECG"]

# plotting the power specral density for the right hand of the first participant's ECG signal while watching clip 1
f, Pxx_den = signal.welch(rightHandECG_1, fsECG_1)  # any idea on haow to set nperseg ???
# considering PSD within 0-40 Hz
f = f[:41]
Pxx_den = Pxx_den[:41]
plt.semilogy(f, Pxx_den)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()
