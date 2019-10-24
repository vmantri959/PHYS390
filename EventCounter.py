import pandas as pd
import matplotlib.pyplot as p
import numpy as np

#Getting Data
waterfile = pd.read_hdf("/home/vmantri/darkmatter/cache_files/watertank_01_2018_alan.hdf5")
waterfile.query('83 >= PMTs_length >=8 ', inplace = True)
tStart =(list(waterfile.iloc[:,6]))
tStart.sort()

#This code simply counts the number of events in each day and plots it

nano = 8.64E+13 #number of nanoseconds in a day
startTime = 1514794706000002840 #January 1st 8:00
endTime = 1517386706000002840 #January 31 8:00
   
day_events = [] #array with each element containing the number of events of each day
count = 0

for i in tStart:
    if(i - startTime < nano) and i < endTime:
        count = count + 1
    elif (i < endTime):
        day_events.append(count)
        count = 1
        startTime = startTime + nano
    else:
        day_events.append(count)
        break
    
#Plotting    
day = []

for i in range(1, len(day_events) + 1):
    day.append(i)

p.figure(1)
p.plot(day, day_events)
p.xlabel('Day Number in January')
p.ylabel('Events in the Day')
p.title('Number of events in each day')
p.show()
print(day_events)
