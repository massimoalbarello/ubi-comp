import pickle
import numpy as np
from scipy import signal
import utils



with open("./ex2_recordings/participant_01.pkl", "rb") as f:
    participant_1_data = pickle.load(f)

# print(participant_1_data["recordings"][1]["EMO"])

# create EMO array with 22 elements, each element is an array containing all the values of a particular face landmark feature
emo_array = []
for element in participant_1_data["recordings"][1]["EMO"][0]:
    emo_array.append([element, ])

for sample in participant_1_data["recordings"][1]["EMO"][1:]:
    for i, element in enumerate(sample):
        emo_array[i].append(element)

# print(emo_array)

utils.statisticalMeasurements(emo_array[1], 'vertical deformation of the upper lip')
utils.statisticalMeasurements(emo_array[2], 'vertical deformation of the lower lip')
utils.statisticalMeasurements(emo_array[3], 'horizontal deformation of the left lip corner')
utils.statisticalMeasurements(emo_array[4], 'vertical deformation of the left lip corner')
utils.statisticalMeasurements(emo_array[5], 'horizontal deformation of the right lip corner')
utils.statisticalMeasurements(emo_array[6], 'vertical deformation of the right lip corner')
utils.statisticalMeasurements(emo_array[7], 'deformation of the right eyebrow')
utils.statisticalMeasurements(emo_array[8], 'deformation of the left eyebrow')
utils.statisticalMeasurements(emo_array[9], 'deformation of the right cheek')
utils.statisticalMeasurements(emo_array[10], 'deformation of the left cheek')
utils.statisticalMeasurements(emo_array[11], 'deformation of the right lid')
utils.statisticalMeasurements(emo_array[12], 'deformation of the left lid')










