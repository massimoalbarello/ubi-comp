# Answers

## Task 1 - Submission
``` 
TASK 1 - RESULTS
-----------
Question 1:
-----------
Shortest sensor log: ankle
Total duration: 451008
Duration at Jungfraujoch: 206956

Portion of trip spent in Jungfraujoch: 45.9 %
-----------
Question 2:
-----------
The average displacement between:
wrist and chest measurements is: 54.470 with a standard deviation of: 3.754
head and chest measurements is: 149.590 with a standard deviation of: 12.239
ankle and chest measurements is: 167.700 with a standard deviation of: 8.707

Points removed from:
Wrist signal: 54
Head signal: 149
Ankle signal: 167
Chest signal: 0
-----------
Question 3:
-----------
Rates obtained by visual inspection: 12.60 , 13.64, 12.49

The sample rate is: 12.91 Hz

```
## Task 1 - Solutions

* Samples removed from each trace to synchronize:
    * chest: 0
    * wrist: 56
    * ankle: 174
    * head: 119

* Sampling frequency of the sensors: 13.7 Hz

## Task 2 - Submission

(1) Travel day: 16th dec 2020

**Reasoning:**
We identified in the data plot the plateau with the lowest pressure: that corresponds to the pressure at the level of the observatory (3572m) which is at similar altitude to the weather station taking official measurements(3576m). The day of the visit is the day where the pressure measured at the observatory is closest to the data we measure at the observatory, which is the 16th of December.

(2) Starting point: Grindelwald

**Reasoning:** 

From visual inspection we split the curve into sections that correspond to different activities: flat areas correspond to waiting times between transport(s) or staying at the top and slopes correspond to travel time. Using the sample rate we estimate travel time and using an open source library (pvlib) we estimate the altitude from air pressure. From these we deduced that the journey to Jungfraujoch starts at around 1000m altitude, then stops after roughly 20min at an altitude of around 2300m for 5min before reaching Jungfraujoch after another 20min trip. Cross checking with the SBB schedule and Google maps for possible itineraries, we concluded that Grindelwald was the most likely starting point and that the subject took the route through Eigergletscher to Jungfraujoch.

(3)
Laterbrunnen: False, Zurich: true, Luzern: true, Basel: false, Bern: False, interlaken: true, Wengen: false, Grindelwald: true, Kleine Sheidegg: False

**Reasoning:** 

- Using the same curve segmentation approach as the previous question, we can tell the subject most likely took the same way down Jungrfraujoch as they came up. By matching estimated altitudes to travel time, we can infer the subject probably took the route down to Grindelwald through Eigergletscher.
- Given this route we can exclude Kleine Scheidegg (2061m) : the route between Grindelwald (1034m) and Eigergletscher(2320m) is direct both ways and doen't pass through Kleine Scheidegg. 
- From Grindelwald, we know the subject traveled for about 2h before turning off the sensors: from duration alone we can exclude Basel, which by car or public transit is at least 2.5h away from Grindelwald. 
- Bern, Luzern and Zurich are all possible within driving or train distance, and the route to any of them would pass through Interlaken. Cross checking travel time and expected altitude with the itineraries validates that the subject possibly passed through Interlaken. 
- The trip from Interlaken to Bern however, doesn't involve the altitude changes that the sensors show (at around 45min away from Grindelwald), so we can conclude the subject probably did not pass through Bern. Instead, Going to Luzern or Zurich is possible within 2h and involves passing over an elevated area at around 1000m ( near Brünig-Hasliberg) which matches the pressure drop in the curve towards the later part of the trip. A possible itenerary could be that the subject drove a car from Grindelwald to Zurich passing through Interlaken and Luzern, the estimated altitude at the end of the trip (~460m) being close to Zurich's (~408m). 
- Accessing Wengen and Lauterbrunnen would require spending longer times at higher altitudes which doesn't match the measurement profile, so we can also rule them out. 


## Task 2 - Solutions

* The subject started his journey at Grindelwald Terminal, taking the cablecar to
Eigergletscher and from there the train to Jungfraujoch. The return journey was identical
back to Grindelwald Terminal, from where the subject took a car and drove the fastest route
to Zurich (over Brünigpass).
* The journey did take place on 16.12.2020.

## Task 3 - Submission 

(1) Max speed of elevator:
 
**Answer:**
```
--------------------------------
Question 3.1 :
--------------------------------
Maximum speed of elevator going up: 6.29 m/s
Maximum speed of elevator going down: 6.73 m/s
```

**Reasoning:**
We can convert the pressure information into elevation data, which corresponds to vertical displacement (in meters). By taking the first derivative of the elevation (and multiplying it by the sample rate) we get the vertical velocity in meters per second. The using a 1D convolution filter over a window of 3 seconds, we obtain the moving average of vertical velocity. By visual inspection, we select intervals of interests corresponding to the elevator rides. The maximum speed going up is the maximum 3s average in the "elevator going up" interval, and the maximum speed going down is the minimum 3s average in the "elevator going down" interval. 

For sanity check, we know from the website that the elevator needs 25 seconds to travel 108m, so we know the peak speed should be larger than 108/25 = 4.32 m/s.

(2) IMU sample rate: 

**Answer:**
```
--------------------------------
Question 3.2 :
--------------------------------
IMU sampling rate: 128.0 Hz

```
**Reasoning:**

Under the assumption that all sensors on a device turn on and off at the same time, thenthe 'Chest' sensor and the IMU are recording data for the same duration. We can get the time by dividing the number of samples in the Chest trace by the sampling rate from task 1 (13.7 Hz), then get the IMU sampling rate by dividing the total number of samples in the IMU recording by the time. 

3) Percentage of time spent walking and number of steps

**Answer:**
```
--------------------------------
Question 3.3:
--------------------------------
Percentage of the trip spent walking: 9.6 %
Number fo steps taken: 5439
```
**Reasoning:**

When the subject is walking, the accelerometer signal is expected to oscillations of amplitude larger that the noise when standing/sitting still or in a vehicle. We can therefore identify the sections in which the subject is walking by looking at the signal variance. From the information we know about the itinerary, we can narrow down the areas in which we expect the subject to not be walking ((ex: car ride from Grindelwald to Zurich) and by observing a smoothed variance plot, we can determine a threshold above which high variance signals walking. Sections in the variance plot with values above the threshold and separated by more than 0.4s are marked as individual walking sections. Their duration is summed and divided by the total IMU signal duration to get the percentage of walking time. Walking patterns are periodical so we can count the number of steps bu counting periodic peaks inside walking intervals. We can do that using scipy.signal find_peaks function and then add up the number of peaks found in every interval to get the step count.

