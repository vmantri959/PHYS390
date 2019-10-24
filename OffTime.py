
import pandas as pd
import matplotlib.pyplot as p
import numpy as np

#Getting Data
waterfile = pd.read_hdf("/home/vmantri/darkmatter/cache_files/watertank_01_2018_alan.hdf5")
waterfile.query('83 >= PMTs_length >=8 ', inplace = True)
tStart =(list(waterfile.iloc[:,6]))
tStart.sort()

nano = 8.64E+13 # number of nanoseconds in a day
nan = 1.66667E-11 # converts to minutes
startTime = 1514794706000002840 #January 1st 8:00
endTime = 1517386706000002840 #January 31 8:00
missedTime = [] # this array just records the times when the water tanker is off
day_array = [] #maps each element in tStart to the corresponding day

def endOfDay(day, currentTime): #currentTime is tStart[i - 1]
    currentEndTime = startTime + day * nano
    return (currentEndTime - currentTime) * nan

for i in tStart:
    currentDay = int(((i - startTime)/ nano) + 1)
    day_array.append(currentDay)
    
day = 1
timeMissedDay = [] #array which keeps track of the time missed in each day
timeMissed = 0 #element of the above array

for i in range(1, len(tStart) - 1):
    if(tStart[i] <= endTime and ((tStart[i] - tStart[i-1]) > 600E9)):
        missedTime.append((tStart[i] - tStart[i-1]) * nan)   #converting into minutes, this array just records the times when the water tanker is off
        if(day_array[i-1] != day):
            day = day + 1 #Update the day
            timeMissedDay.append(timeMissed) # append final value to array
            timeMissed = 0 # Update it back to 0
        if(day_array[i] == day): # same day, best case 
            timeMissed += (tStart[i] - tStart[i-1]) * nan
        else: # different day
            #First calculate the time between the end of current day and tStart[i - 1], append to the array. Then update 
            #the day, the timeMissedDay array and set timeMissed back to the difference between
            k = endOfDay(day, tStart[i-1])
            timeMissedDay.append(k)
            day = day + 1
            timeMissed = ((tStart[i] - tStart[i-1]) * nan) - k 
    elif(tStart[i] > endTime):
        #Calculate the difference between tStart[i -1] and endTime
        timeMissed += (endTime - tStart[i-1]) * nan
        timeMissedDay.append(timeMissed)
        break
    else:
        #Make sure that the day is the same as day_array[i - 1]
        if(day_array[i-1] != day):
            day = day + 1 #Update the day
            timeMissedDay.append(timeMissed)
            timeMissed = 0

