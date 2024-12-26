#! /usr/bin/env python3
import serial
import time
import os
import threading
import queue
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import datetime

matplotlib.rc('xtick', labelsize=8)     
matplotlib.rc('ytick', labelsize=10)


global log
log = 0 # set log to 1 to save a log in RAM.

t = datetime.datetime.now()
if os.path.exists('/dev/ttyAMA0') == True:
    ser = serial.Serial(port='/dev/ttyAMA0',baudrate = 9600,parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#if os.path.exists('/dev/ttyAMA1') == True:
#     ser = serial.Serial(port='/dev/ttyAMA1',baudrate = 9600,parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#if os.path.exists('/dev/ttyUSB0') == True:
#    ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 9600,parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#if os.path.exists('/dev/ttyUSB1') == True:
#     ser = serial.Serial(port='/dev/ttyUSB1',baudrate = 9600,parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#if os.path.exists('/dev/ttyACM0') == True:
#    ser = serial.Serial(port='/dev/ttyACM0',baudrate = 9600,parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#if os.path.exists('/dev/ttyACM1') == True:
#     ser = serial.Serial(port='/dev/ttyACM1',baudrate = 9600,parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

if os.path.exists('/run/shm/example.txt'): # note log currently saved to RAM
   os.remove('/run/shm/example.txt')       # and gets deleted as you start the script
   
def thread_read():
   global ser, xs,y1,y2,y3,y4,y5, max_count, count, t
   max_count = 600
   count = 0
   count2 = 0
   xs = []
   y1 = []
   y2 = []
   y3 = []
   y4 = []
   y5 = []
   while True:
       #read data from arduino
       Ard_data = ser.readline()
       Ard_data = Ard_data.decode("utf-8","ignore")
       counter1 = Ard_data.count(' ')
       counter2 = Ard_data.count('.')
       # check for 4 spaces  and 5 data vaules
       if counter1 == 4 and counter2 == 5:
           b,c,d,e,f= Ard_data.split(" ")
           # save to log file
           if log == 1:
               now = datetime.datetime.now()
               timestamp = now.strftime("%y/%m/%d-%H:%M:%S")
               with open('/run/shm/example.txt', 'a') as g:
                   g.write(timestamp + "," + str(count)+"," + Ard_data + "\n")
           # write to lists
           xs.append(str(datetime.datetime.now())[11:19])
           y1.append(float(b))
           y2.append(float(c))
           y3.append(float(d))
           y4.append(float(e))
           y5.append(float(f))
           # delete old list values
           if len(xs) > max_count:
               del xs[0]
               del y1[0]
               del y2[0]
               del y3[0]
               del y4[0]
               del y5[0]
           count +=1

def thread_plot():
       global fig,animate, ax1
       fig = plt.figure()
       ax1 = fig.add_subplot(1,1,1)
       ani = animation.FuncAnimation(fig, animate, interval=1000)
       plt.show()
   
def animate(i):
       global xs,y1,y2,y3,y4,y5,max_count, count
       if count > 0 and len(xs) == len(y1) == len(y2) == len(y3) == len(y4) == len(y5):
           ax1.clear()
           plt.xlabel('Time') 
           plt.ylabel('dB')
           ax1.xaxis.set_major_locator(MultipleLocator(30))
           ax1.xaxis.set_minor_locator(MultipleLocator(10))
           ax1.plot(xs, y1, '-.b', label='Avg')
           ax1.plot(xs, y2, '-r', label='A0')
           ax1.plot(xs, y3, '-g', label='A0Slow')
           ax1.plot(xs, y4, ':c', label='Min')
           ax1.plot(xs, y5, ':y', label='Max')
           ax1.legend(loc='upper left')
           plt.gcf().autofmt_xdate()

read_thread = threading.Thread(target=thread_read)
read_thread.start()

plot_thread = threading.Thread(target=thread_plot)
plot_thread.start()
