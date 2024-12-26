#!/usr/bin/env python

import sys
import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial

#initialize serial port
ser = serial.Serial()
ser.port = '/dev/cu.usbmodem2101' #Arduino serial port
ser.baudrate = 2000000
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nSerial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

MAXCOUNT = float(2 ** 24)
MIDCOUNT = float(MAXCOUNT // 2)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] # time
y1 = [] 
y2 = [] 
_, tsec0 = math.modf( time.time_ns() / 1.0e9 )


TMAX = 0.100 # seconds
sliding = False
xbeg = 0.0
xend = TMAX

# This function is called periodically from FuncAnimation
def animate(i, xs, y1, y2):

    #Aquire and parse data from serial port
    line=ser.readline().decode().strip()
    #print('line:', line)
    fields=line.split(' ')
    #print('fields:', fields)
    if len(fields) < 2: return
    tfrac, tsec = math.modf( time.time_ns() / 1.0e9 )
    t = (tsec - tsec0) + tfrac
    ich1 = int(fields[0])
    ich2 = int(fields[1])
    ch1 = float(ich1) / MIDCOUNT
    ch2 = float(ich2) / MIDCOUNT
    #print(f't, ch1, ch2:  {t:6.6f},    ' \
    #     f'{ich1:10.0f}, {ich2:10.0f}    ' \
    #     f'{ch1:8.3f}, {ch2:8.3f}' )
    #sys.exit()

    # Limit x and y lists to 20 items
    sliding = t > TMAX
    xlen =  len(xs)

	  # Add x and y to lists
    xs.append(t)
    y1.append(ch1)
    y2.append(ch2)

    if sliding:
      xend = t
      xbeg = t - TMAX
      xs = xs[-xlen:]
      y1 = y1[-xlen:]
      y2 = y2[-xlen:]
    else:
      xbeg = 0.0
      xend = TMAX

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, y1, label="Channel 1")
    ax.plot(xs, y2, label="Channel 2")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Stereo Metering')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.axis([xbeg, xend, -1.2, 1.2]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(), interval=0.01, save_count=100)
ani = animation.FuncAnimation(fig, animate, fargs=(xs, y1, y2), interval=0.01)


plt.show()
