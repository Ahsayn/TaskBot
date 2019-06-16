# -*- coding: utf-8 -*-

"""
@author: Nyasha Kapfumvuti
Soft Real Time Operating System Control Loop Practice
Adjusts frames for any errors from interrupts or otherwise

Based on Artificial Intelligence for Robotics Course from PacktPub
"""

import time
import math
import matplotlib.pyplot as plt
from numpy import mean

# Highest required frequency in robot Control
FRAMERATE = 30
# Single frame period
FRAME = 1.0/FRAMERATE
# Duration of entire sim
counter = 2000
# Capture Timestamps
myTimer = 0.0
# hold error adjustment val
TIME_CORRECTION = 0.0
# hold data
dataStore = []

# Notify: Ready
print("Start Counting:  Frame time: ", FRAME, "Run time: ", FRAMERATE*counter)
# initialize timer
currentTime = time.time()
masterTime = currentTime
frameCounter = 0

# begin control loop
for i in range(counter):
    # create some delays (artificial time waster)
    for j in range(1000):
        x = 120
        y = 42 * i
        z = math.cos(x)
        o = math.sin(y)
    
    # increment counter and record time after delay
    frameCounter += 1

    # check if frame completed
    if frameCounter % FRAMERATE == 0:
        print("Frame ", frameCounter, " completed")
    
    # measure elapsed time and make advance delay adjustment as need
    timeUpdate = time.time()
    myTimer = timeUpdate - currentTime
    # margin of time left before frame ends
    timeError = FRAME - myTimer

    # sleep program to wait for next frame start (and allow other OS tasks to be done)
    # Note that proportional control (/2) is used to stop adjustment from causing oscillation
    # (Similar to oversteering clock and ensuring smaller steps that lead to convergance)

    sleeptime = timeError + (TIME_CORRECTION/2.0)

    # ensure that required offset is a +ve value
    sleeptime = max(sleeptime, 0.0)
    
    # put program process to sleep for amount needed to next frame
    time.sleep(sleeptime)

    # prep for next frame ops
    timeUpdate = time.time()
    measuredFrameTime = timeUpdate - currentTime
    TIME_CORRECTION = FRAME - measuredFrameTime
    dataStore.append(measuredFrameTime*1000)

    timeUpdate = time.time()
    # loop ends

endTime = time.time() - masterTime
avgTime = endTime / counter
print("FINISHED COUNTING")
print("REQUESTED FRAME TIME: ", FRAME, "AVERAGE FRAME TIME: ", avgTime)
print("REQUESTED TOTAL TIME:",FRAME*counter,"ACTUAL TOTAL TIME:", endTime)
print("AVERAGE ERROR",FRAME-avgTime, "TOTAL_ERROR:",(FRAME*counter) - endTime)
print("AVERAGE SLEEP TIME: ",mean(dataStore),"AVERAGE RUN TIME",(FRAME*1000)-mean(dataStore))

n, bins, patches = plt.hist(dataStore, 50, normed=1, facecolor='green', alpha=0.75)
plt.show()
plt.plot(dataStore)
plt.show()



