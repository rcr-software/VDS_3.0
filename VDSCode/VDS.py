
#import Libraries
import time
import threading
import os
import subprocess
from tkinter import* 
import RPi.GPIO as GPIO
import adafruit_ssd1306
import busio
import board
from digitalio import DigitalInOut, Direction, Pull

from picamera import PiCamera

import VectorNav.vectornavLib
import ultGPS.GPS
import PressureSensor.BMP280
import Telemetry.RFM9X
import Button.button
import System.system


v=VectorNav.vectornavLib.vnav()
g=ultGPS.GPS.GPS()
b=PressureSensor.BMP280.BMP()
t=Telemetry.RFM9X.telemetry()
c=Button.button.buttonOps()
s=System.system.systemRead()

#Global Variables
vertVel = 0


longDec=38.2527                      
latDec=85.7585                       
bmp280Alt=0
vertAccel=0
yaw=0
pitch=0
roll=0
CPUTemp=0
CPULoad=0
usedRAM = 0
gpsfix=0
pressure=0
battery=0
local_rssi=0
frequency=915                         
temp1=0
temp2=0
temp3=0
press1=0
press2=0
press3=0
noid1=0
noid2=0
noid3=0
noid4=0
noid5=0
noid6=0
noid7=0

packetNum=0
sendState=1

#############################################

# Setup i2c bus  sudo i2cdetect -y 1
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
display.fill(0)
display.show()
width = display.width
height = display.height

#setup the Camera [test for cmd: raspivid -o video.h264 -t 10000]
#camera = PiCamera()
#camera.start_recording("testvid.h264")
      
#initialize threads
systemLoads = threading.Thread(target = s.systemLoads)
readGPS = threading.Thread(target = g.readGPS)
telemetrySend = threading.Thread(target = t.telemetrySend)
telemetryReceive = threading.Thread(target = t.telemetryReceive)
readVnav = threading.Thread(target = v.readVnav)
comm = threading.Thread(target = c.comm)
BMP = threading.Thread(target = b.readBMP)
#################################################


t.radioCheck() #check to see if the radio is on
print("radio check sucsesful")

#start threads
readVnav.start() #read vnav data
comm.start()
readGPS.start()#read gps data
telemetryReceive.start()
systemLoads.start()
telemetrySend.start()
BMP.start()

while 1: # this whle loop kills the threads and executes the rest of the program.
     if c.btnValA == 1:
         time.sleep(1)
         break

print("The End")

v.vnavTxtClose()


#close active threads

#close active threads

#camera.stop_recording()

#gpsDecimalFile.close()
