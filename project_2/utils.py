from scipy import signal, stats
import numpy as np


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
