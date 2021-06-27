import math
import time

import os
import subprocess

import serial
from tkinter import* 
from time import sleep
import RPi.GPIO as GPIO
import numpy

import smbus
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import busio



gps = serial.Serial(
        port='/dev/ttyS0',# ttyS0/ttyAMA0 for the serial line and ttyUSB0 for the usb port
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1 
)


while 1:
    global longDec, latDec, gpsAltitude
    y = str(gps.readline())
    print(y)    
    gpsStateRMC = "$GPRMC" in y
    gpsStateGGA = "$GPGGA" in y
        
    if (gpsStateGGA == 1):
        y = y.split(',')
        gpsAltitude = str(float(y[7]))
            
    if(gpsStateRMC == 1):
        gpsNMEAFile = open("NMEA_Data","a")
        gpsNMEAFile.write(y)
        gpsNMEAFile.write('\n')
            
        y = y.split(',')
        latNMEA = float(y[3])
        latDirectionNMEA = str(y[4])
        longNMEA = float (y[5])
        longDirectionNMEA = str(y[6])
            
        #detrmine the decimal degrees direction
        if (longDirectionNMEA == "W"):
            longDirectionDec = -1
        else:
            longDirectionDec = 1
                
        if (latDirectionNMEA == "N"):
            latDirectionDec = 1
        else:
            latDirectionDec = -1
            
        #determine the decimal degrees magnitude
        latDec = round( latDirectionDec * (math.floor(latNMEA / 100) + (latNMEA - ((math.floor(latNMEA / 100)) * 100)) / 60), 4)   
        longDec = round( longDirectionDec * (math.floor(longNMEA / 100) + (longNMEA - ((math.floor(longNMEA / 100)) * 100)) / 60), 4)
            
        #ensure the use of trailing zeros for 4 decimal places
        temp = '{:<04}'
        latDec = str(temp.format(latDec))
        longDec = str(temp.format(longDec))
        
            
