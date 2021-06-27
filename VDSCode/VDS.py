
#import Libraries
import time
import threading
import os
import subprocess
from tkinter import* 
from picamera import PiCamera

import VectorNav.vectornavLib
import ultGPS.GPS
import PressureSensor.BMP280
import Telemetry.RFM9X
import Button.button
import System.system
import Display.display
import Velocity.velocity
import RocketConstants as rocket

v=VectorNav.vectornavLib.vnav()
g=ultGPS.GPS.GPS()
b=PressureSensor.BMP280.BMP()
t=Telemetry.RFM9X.telemetry()
c=Button.button.buttonOps()
s=System.system.systemRead()
d=Display.display.oled()
vel=Velocity.velocity.velocity()
#############################################
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

d.displayStats()
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

while c.btnValA == 0: # this whle loop kills the threads and executes the rest of the program.
    time.sleep(1)
    #(round(b.readBMP(),4))
    print(vel.velocity_h(rocket.c, 1000, 200, 10000))
print("The End")

v.vnavTxtClose()

#close active threads

#close active threads

#camera.stop_recording()

#gpsDecimalFile.close()
